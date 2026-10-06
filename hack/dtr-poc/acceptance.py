#!/usr/bin/env python3
# #############################################################################
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
# #############################################################################
"""Run BaSyx tenant acceptance exclusively in a newly created disposable Kind cluster."""
import argparse
import base64
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

import yaml

from api_contract import Api, crud, encoded, fixture, read_persisted
from default_regression import verify as default_regression
from fixtures import DATABASE, PG_IMAGE, database_resources
from tenant_profile import ROOT, profile

NODE_IMAGE = "kindest/node:v1.30.0@sha256:047357ac0cfea04663786a612ba1eaba9702bef25227a794b52890dd8bcd692e"
NAMESPACES = ("basyx-poc", "umbrella-basyx-poc")


class Acceptance:
    def __init__(self, artifacts, temporary):
        self.artifacts, self.temporary = artifacts, temporary
        self.cluster = "basyx-poc-" + secrets.token_hex(4)
        self.context = "kind-" + self.cluster
        self.kubeconfig = temporary / "kubeconfig"
        self.secret_values, self.created = [], False
        self.commands, self.results = [], {"result": "RUNNING", "checks": {}, "tenants": []}
        self.events = []
        self.environment = {**os.environ, "KUBECONFIG": str(self.kubeconfig)}
        self.renderer = ["--post-renderer", sys.executable, "--post-renderer-args",
                         str(ROOT / "hack/dtr-poc/post-render.py")]

    def redact(self, text):
        text = text.replace(str(self.kubeconfig), "<temporary-kubeconfig>")
        for value in self.secret_values:
            text = text.replace(value, "<redacted>").replace(base64.b64encode(value.encode()).decode(), "<redacted>")
        return text

    def run(self, *args, input=None, quiet=False, check=True, timeout=600):
        command = list(map(str, args))
        if command[0] in {"helm", "kubectl"}:
            context_flag = "--kube-context" if command[0] == "helm" else "--context"
            # Global flags must precede `exec --`, otherwise they reach psql/sh.
            command = [command[0], "--kubeconfig", str(self.kubeconfig), context_flag, self.context, *command[1:]]
        result = subprocess.run(command, input=input, text=True, encoding="utf-8", errors="replace", capture_output=True,
                                env=self.environment, timeout=timeout)
        self.commands.append({"argv": [self.redact(x) for x in command], "exitCode": result.returncode})
        if not quiet:
            output = self.redact(result.stdout + result.stderr)
            if output.strip():
                print(output.strip(), flush=True)
        if check and result.returncode:
            # No raw application logs, credentials, or manifests in failure output.
            raise RuntimeError(f"Command failed ({result.returncode}): {self.redact(' '.join(command))}")
        return result.stdout if check else result

    def get(self, namespace, kind, name=None):
        args = ["kubectl", "get", kind]
        if name:
            args.append(name)
        return json.loads(self.run(*args, "-n", namespace, "-o", "json", quiet=True))

    def apply(self, objects):
        self.run("kubectl", "apply", "-f", "-", input=yaml.safe_dump_all(objects, sort_keys=False), quiet=True)

    def save(self, name, value):
        self.artifacts.joinpath(name).write_text(self.redact(json.dumps(value, indent=2)) + "\n", encoding="utf-8")

    def prepare(self):
        self.results["versions"] = {
            "helm": self.run("helm", "version", "--short", quiet=True).strip(),
            "kind": self.run("kind", "version", quiet=True).strip(),
            "python": sys.version.split()[0], "nodeImage": NODE_IMAGE, "postgresImage": PG_IMAGE,
            "basyxChart": "3.15.0", "basyxApp": "1.1.0"}
        existing = self.run("kind", "get", "clusters", quiet=True).splitlines()
        assert self.cluster not in existing
        # Never connect to the user's current Kubernetes context.
        self.created = True  # Clean up even if Kind creation fails partway through.
        self.run("kind", "create", "cluster", "--name", self.cluster, "--image", NODE_IMAGE,
                 "--kubeconfig", self.kubeconfig, "--wait", "120s")
        assert self.run("kubectl", "config", "current-context", quiet=True).strip() == self.context
        nodes = json.loads(self.run("kubectl", "get", "nodes", "-o", "json", quiet=True))["items"]
        assert len(nodes) == 1 and nodes[0]["metadata"]["name"] == self.cluster + "-control-plane"
        self.node = nodes[0]["metadata"]["name"]
        self.results["versions"]["kubernetes"] = nodes[0]["status"]["nodeInfo"]["kubeletVersion"]

    def provision(self, namespace, tenant):
        values, metadata = profile(namespace, "basyx-dtr-poc", tenant)
        path = self.artifacts / f"{namespace}-values.yaml"
        path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
        metadata["values"] = path
        self.run("docker", "exec", self.node, "install", "-d", "-m", "0700", "-o", "999", "-g", "999",
                 f"/var/local/dtr-poc/{namespace}/{metadata['postgres']}", quiet=True)
        self.apply([database_resources(metadata)[0]])
        admin_password, app_password = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        self.secret_values += [admin_password, app_password]
        connection = {"host": metadata["postgres"], "port": "5432", "dbname": DATABASE,
                      "user": DATABASE, "password": app_password, "searchPath": DATABASE,
                      "jdbc-uri": f"jdbc:postgresql://{metadata['postgres']}:5432/{DATABASE}", "sslmode": "disable"}
        self.apply([{"apiVersion": "v1", "kind": "Secret", "type": "Opaque",
                     "metadata": {"name": name, "namespace": namespace}, "stringData": data}
                    for name, data in ((f"{metadata['postgres']}-admin", {"password": admin_password}),
                                       (metadata["databaseSecret"], connection))])
        # Passwords remain in process memory and kubectl stdin only.
        metadata["app_password"] = app_password
        self.apply(database_resources(metadata)[1:-1])
        self.run("kubectl", "wait", "-n", namespace, "--for=condition=Ready",
                 f"pod/{metadata['postgres']}-0", "--timeout=180s")
        self.apply(database_resources(metadata)[-1:])
        self.run("kubectl", "wait", "-n", namespace, "--for=condition=Complete",
                 f"job/{metadata['postgres']}-bootstrap", "--timeout=120s")
        self.run("helm", "lint", ROOT / "charts/tx-data-provider", "-f", path)
        rendered = self.run("helm", "template", "basyx-dtr-poc", ROOT / "charts/tx-data-provider",
                            "-n", namespace, "-f", path, *self.renderer, quiet=True)
        objects = [o for o in yaml.safe_load_all(rendered) if o]
        assert {o["kind"] for o in objects} <= {"Secret", "ConfigMap", "ServiceAccount", "Service", "Deployment", "Job"}, "Unexpected BaSyx resource type"
        assert sum(o["kind"] == "Deployment" for o in objects) == 1
        job = next(o for o in objects if o["kind"] == "Job")
        assert job["metadata"]["annotations"]["helm.sh/hook"] == "pre-install,pre-upgrade"
        assert job["spec"]["template"]["spec"]["serviceAccountName"] == metadata["fullname"]
        # Invalid dual selection must fail before Kubernetes can receive a manifest.
        bad = self.run("helm", "template", "invalid", ROOT / "charts/tx-data-provider", "-f", path,
                       "--set", "digital-twin-bundle.enabled=true", quiet=True, check=False)
        assert bad.returncode and "select exactly one DTR" in bad.stderr
        self.results["checks"]["dualSelectionRejected"] = "PASS"
        return metadata

    def install(self, tenant):
        print(f"Installing {tenant['tenant']} in {tenant['namespace']}", flush=True)
        self.run("helm", "install", tenant["release"], ROOT / "charts/tx-data-provider",
                 "-n", tenant["namespace"], "-f", tenant["values"], *self.renderer, "--wait", "--timeout", "5m")
        ns, full = tenant["namespace"], tenant["fullname"]
        job = self.get(ns, "job", full + "-configuration")
        assert job["status"].get("succeeded") == 1
        pods = self.get(ns, "pods")["items"]
        pod = next(p for p in pods if p["metadata"].get("labels", {}).get("app.kubernetes.io/component") == "digital-twin-registry")
        status = pod["status"]["containerStatuses"][0]
        assert status["ready"] and status["restartCount"] == 0
        assert status["state"]["running"]["startedAt"] >= job["status"]["completionTime"]
        tenant["deployment"] = self.get(ns, "deployments")["items"][0]["metadata"]["name"]
        if not any(t["namespace"] == ns for t in self.results["tenants"]):
            observed = {k: tenant[k] for k in ("tenant", "namespace", "release", "apiBase", "databaseSecret", "postgres")}
            observed.update(dtrImage=pod["spec"]["containers"][0]["image"],
                            dtrImageID=status.get("imageID"), coldStartRestarts=status["restartCount"],
                            initializedAt=job["status"]["completionTime"],
                            dtrStartedAt=status["state"]["running"]["startedAt"])
            self.results["tenants"].append(observed)
        self.results["checks"]["coldStartZeroRestarts-" + ns] = "PASS"

    def failed_initialization(self, tenant):
        values = yaml.safe_load(tenant["values"].read_text())
        values["digital-twin-basyx-bundle"]["basyx"]["configurationService"] = {
            "command": ["/poc-intentionally-nonexistent"], "backoffLimit": 0,
            "activeDeadlineSeconds": 20, "restartPolicy": "Never"}
        path = self.temporary / "failed-init-values.yaml"
        path.write_text(yaml.safe_dump(values), encoding="utf-8")
        result = self.run("helm", "install", tenant["release"], ROOT / "charts/tx-data-provider",
                          "-n", tenant["namespace"], "-f", path, *self.renderer,
                          "--wait", "--timeout", "60s", quiet=True, check=False)
        assert result.returncode and not self.get(tenant["namespace"], "deployments")["items"]
        self.run("helm", "uninstall", tenant["release"], "-n", tenant["namespace"])
        self.results["checks"]["failedInitializationBlocksDtr"] = "PASS"
        print("Failed initialization blocked DTR creation: PASS", flush=True)

    @contextmanager
    def forward(self, tenant, events):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        process = subprocess.Popen([shutil.which("kubectl"), "--kubeconfig", str(self.kubeconfig),
            "--context", self.context, "-n", tenant["namespace"], "port-forward", "--address=127.0.0.1",
            "service/" + tenant["service"], f"{port}:8080"], env=self.environment,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.commands.append({"argv": ["kubectl", "port-forward", "-n", tenant["namespace"],
                                       "service/" + tenant["service"], "<loopback-port>:8080"], "exitCode": None})
        try:
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError("Loopback port forwarding exited")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                        break
                except OSError:
                    time.sleep(0.3)
            else:
                raise RuntimeError("Loopback port forwarding timed out")
            yield Api(f"http://127.0.0.1:{port}/digital-twin-registry", events)
        finally:
            process.terminate()
            process.wait(timeout=10)

    def sql(self, tenant, sql):
        return self.run("kubectl", "exec", "-i", "-n", tenant["namespace"],
                        tenant["postgres"] + "-0", "--", "psql", "-U", "postgres", "-d", DATABASE,
                        "-X", "-tA", "-v", "ON_ERROR_STOP=1", input=sql, quiet=True).strip()

    def restart(self, tenant):
        ns, name = tenant["namespace"], tenant["postgres"] + "-0"
        old = self.get(ns, "pod", name)["metadata"]["uid"]
        self.run("kubectl", "delete", "pod", name, "-n", ns, "--wait=true")
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            result = self.run("kubectl", "get", "pod", name, "-n", ns, "-o", "json", quiet=True, check=False)
            if result.returncode == 0:
                pod = json.loads(result.stdout)
                if pod["metadata"]["uid"] != old and any(c["type"] == "Ready" and c["status"] == "True"
                                                          for c in pod["status"].get("conditions", [])):
                    break
            time.sleep(2)
        else:
            raise RuntimeError("PostgreSQL replacement did not become Ready")
        self.run("kubectl", "rollout", "restart", "deployment/" + tenant["deployment"], "-n", ns)
        self.run("kubectl", "rollout", "status", "deployment/" + tenant["deployment"], "-n", ns, "--timeout=120s")

    def retention(self, tenant):
        resources = [("secret", tenant["databaseSecret"]), ("persistentvolumeclaim", tenant["postgres"]),
                     ("statefulset", tenant["postgres"])]
        return {f"{kind}/{name}": self.get(tenant["namespace"], kind, name)["metadata"]["uid"]
                for kind, name in resources}

    def finish(self):
        try:
            if self.created:
                self.run("kind", "delete", "cluster", "--name", self.cluster, "--kubeconfig", self.kubeconfig)
                assert self.cluster not in self.run("kind", "get", "clusters", quiet=True).splitlines(), "Temporary Kind cluster remains"
                self.results["checks"]["temporaryClusterRemoved"] = "PASS"
        except Exception as error:
            self.results["result"] = "FAIL"
            self.results["checks"]["temporaryClusterRemoved"] = "FAIL"
            self.results["cleanupFailure"] = type(error).__name__ + ": " + self.redact(str(error))
            raise
        finally:
            self.save("commands.json", self.commands)
            self.save("results.json", self.results)
            self.save("api-events.json", self.events)
            for path in self.artifacts.iterdir():
                if not path.is_file():
                    continue
                raw = path.read_text(encoding="utf-8")
                for value in self.secret_values:
                    assert value not in raw and base64.b64encode(value.encode()).decode() not in raw, "Secret artifact leak"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", required=True, type=Path)
    args = parser.parse_args()
    artifacts = args.artifacts.resolve()
    if artifacts.exists() and any(artifacts.iterdir()):
        parser.error("Use a new empty artifact directory for each run")
    artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="basyx-dtr-poc-") as folder:
        test = Acceptance(artifacts, Path(folder))
        try:
            test.results["checks"]["defaultTractusX"] = default_regression(ROOT, Path(folder) / "baseline", test.run)
            test.prepare()
            tenants = [test.provision(ns, "poc-a" if i == 0 else "poc-b") for i, ns in enumerate(NAMESPACES)]
            test.failed_initialization(tenants[0])
            for tenant in tenants:
                test.install(tenant)
            token, events, actual = secrets.token_hex(8), test.events, []
            for tenant in tenants:
                with test.forward(tenant, events) as api:
                    actual.append(crud(api, fixture(token, tenant["tenant"])))
            assert actual[0]["id"] == actual[1]["id"] and actual[0]["idShort"] != actual[1]["idShort"]
            # Updating and deleting A's same-ID descriptor cannot alter B's copy.
            with test.forward(tenants[0], events) as api:
                api.call("DELETE", "/shell-descriptors/" + encoded(actual[0]["id"]), expected=204)
                api.call("GET", "/shell-descriptors/" + encoded(actual[0]["id"]), expected=404)
            with test.forward(tenants[1], events) as api:
                read_persisted(api, actual[1])
            with test.forward(tenants[0], events) as api:
                api.call("POST", "/shell-descriptors", fixture(token, tenants[0]["tenant"]), 201)
                actual[0] = api.call("GET", "/shell-descriptors/" + encoded(actual[0]["id"]))
            # A's app credential must be rejected by B's separate PostgreSQL instance.
            cross_command = ["kubectl", "exec", "-i", "-n", tenants[0]["namespace"], tenants[0]["postgres"] + "-0",
                "--", "sh", "-c", 'PGPASSWORD=$(cat); export PGPASSWORD; exec psql -h "$1" -U basyx_poc -d basyx_poc -c "SELECT 1" >/dev/null 2>&1',
                "sh", tenants[1]["postgres"] + "." + tenants[1]["namespace"] + ".svc.cluster.local"]
            # Prove the same route is reachable with B's credential first, so a
            # network/DNS failure cannot masquerade as credential isolation.
            test.run(*cross_command, input=tenants[1]["app_password"], quiet=True)
            cross = test.run(*cross_command, input=tenants[0]["app_password"], quiet=True, check=False)
            assert cross.returncode != 0, "Cross-tenant PostgreSQL authentication unexpectedly succeeded"
            test.results["checks"]["independentTenantDataAndCredentials"] = "PASS"
            for i, tenant in enumerate(tenants):
                sql = test.sql(tenant, "SELECT count(*) FROM information_schema.tables WHERE table_schema='basyx_poc';\n"
                    "SELECT rolsuper,rolcreatedb,rolcreaterole FROM pg_roles WHERE rolname='basyx_poc';\n"
                    "SELECT count(*) FROM basyx_poc.aas_descriptor;\n")
                assert sql.splitlines() == ["107", "f|f|f", "1"], sql
                test.save(tenant["namespace"] + "-database.json", {"result": "PASS", "schemaTables": 107,
                          "appRolePrivileged": False, "shellDescriptors": 1})
                test.restart(tenant)
                with test.forward(tenant, events) as api:
                    read_persisted(api, actual[i])
                retained = test.retention(tenant)
                test.run("helm", "upgrade", tenant["release"], ROOT / "charts/tx-data-provider", "-n", tenant["namespace"],
                         "-f", tenant["values"], *test.renderer, "--wait", "--timeout", "5m")
                test.run("helm", "rollback", tenant["release"], "1", "-n", tenant["namespace"], "--wait", "--timeout", "5m")
                with test.forward(tenant, events) as api:
                    read_persisted(api, actual[i])
                test.run("helm", "uninstall", tenant["release"], "-n", tenant["namespace"])
                assert retained == test.retention(tenant)
                test.install(tenant)
                with test.forward(tenant, events) as api:
                    read_persisted(api, actual[i])
                assert retained == test.retention(tenant)
                test.results["checks"]["restartRollbackReinstall-" + tenant["namespace"]] = "PASS"
            test.save("api-events.json", events)
            test.results["result"] = "PASS"
        except Exception as error:
            test.results["result"] = "FAIL"
            test.results["failure"] = type(error).__name__ + ": " + test.redact(str(error))
            raise
        finally:
            test.finish()
    print("BaSyx tenant acceptance: PASS", flush=True)


if __name__ == "__main__":
    main()
