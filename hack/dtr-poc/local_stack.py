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
"""Install Tractus-X DTR and BaSyx DTR side by side in an explicit local test context.

Every kubectl and Helm command receives --context/--kube-context. Generated test
passwords are only sent to kubectl through stdin.
"""
import argparse
import json
import secrets
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

from fixtures import DATABASE, database_resources
from tenant_profile import ROOT, profile

TX_NAMESPACE, TX_RELEASE = "txdtr", "txdtr"
BASYX_NAMESPACE, BASYX_RELEASE, BASYX_TENANT = "basyx", "basyx", "poc"
KEYCLOAK_IMAGE = "quay.io/keycloak/keycloak:26.4.0"
ACCESS_RULES = Path(__file__).parent / "access-rules-tractusx.json"
# Same BaSyx 1.1.0 release as the bundle, but the multi-arch index digests.
MULTI_ARCH = {
    "digitalTwinRegistry": "sha256:aa8bd6fefde0dfc75a74aa7f0d3fce1cc5a5ab90f70a7824ab6ca8d56a9dfa54",
    "configurationService": "sha256:eb01ef0f118054ad1a3eb6081ad9997688523b0ab12d90e87c41592f50318b9d",
    "submodelRepository": "sha256:2b5849cdf759e48cada6b3eba83f826f9117ac0371cd3b6dc8fa50552806cd2f",
}
TX_VALUES = {
    "seedTestdata": False,
    "dataspace-connector-bundle": {"enabled": False, "tractusx-connector": {"enabled": False},
                                   "postgresql": {"enabled": False}, "vault": {"enabled": False}},
}


def issuer():
    return f"http://keycloak.{BASYX_NAMESPACE}.svc.cluster.local:8080/realms/basyx"


def basyx_values(abac):
    values, metadata = profile(BASYX_NAMESPACE, BASYX_RELEASE, BASYX_TENANT)
    basyx = values["digital-twin-basyx-bundle"]["basyx"]
    basyx["digitalTwinRegistry"]["image"] = {"digest": MULTI_ARCH["digitalTwinRegistry"]}
    basyx["configurationService"] = {"image": {"digest": MULTI_ARCH["configurationService"]}}
    service = f"{metadata['fullname']}-submodel-repository"
    basyx["submodelRepository"] = {
        "enabled": True, "image": {"digest": MULTI_ARCH["submodelRepository"]},
        "ingress": {"enabled": False}, "httpRoute": {"enabled": False},
        "environment": {"GENERAL_SUBMODELREGISTRYINTEGRATION": False,
                        "GENERAL_EXTERNALURL": f"http://{service}.{BASYX_NAMESPACE}.svc.cluster.local:8080/submodel-repo"},
        "resources": {"requests": {"cpu": "10m", "memory": "64Mi"}, "limits": {"cpu": "200m", "memory": "256Mi"}},
    }
    if abac:
        basyx["digitalTwinRegistry"]["general"] = {"enableCustomMiddlewareHeaderInjection": True}
        basyx["digitalTwinRegistry"]["abac"] = {
            "enabled": True, "accessRules": ACCESS_RULES.read_text(encoding="utf-8"),
            "trustList": json.dumps([{"issuer": issuer(), "audience": "discovery-service",
                                      "scopes": ["email", "profile"]}], indent=2)}
    return values, metadata


def realm(passwords):
    """Minimal realm: one provider user with all DTR roles and one EDC reader with view only."""
    attribute = lambda name, multivalued=False: {
        "name": name, "multivalued": multivalued,
        "permissions": {"view": ["admin", "user"], "edit": ["admin"]}}
    profile_config = {"attributes": [attribute("username"), attribute("email"), attribute("firstName"),
                                     attribute("lastName"), attribute("role", True)]}
    roles = {"provider": ["view_digital_twin", "add_digital_twin", "update_digital_twin", "delete_digital_twin"],
             "edc-dtr-reader": ["view_digital_twin"]}
    return {
        "realm": "basyx", "enabled": True,
        "components": {"org.keycloak.userprofile.UserProfileProvider": [{
            "providerId": "declarative-user-profile",
            "config": {"kc.user.profile.config": [json.dumps(profile_config)]}}]},
        "clients": [{
            "clientId": "basyx-ui", "publicClient": True, "directAccessGrantsEnabled": True,
            "standardFlowEnabled": False,
            "protocolMappers": [
                {"name": "role", "protocol": "openid-connect", "protocolMapper": "oidc-usermodel-attribute-mapper",
                 "config": {"user.attribute": "role", "claim.name": "role", "multivalued": "true",
                            "jsonType.label": "String", "access.token.claim": "true"}},
                {"name": "audience", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper",
                 "config": {"included.custom.audience": "discovery-service", "access.token.claim": "true"}}]}],
        "users": [{"username": user, "enabled": True, "email": f"{user}@example.invalid", "emailVerified": True,
                   "firstName": user, "lastName": "test", "attributes": {"role": role},
                   "credentials": [{"type": "password", "value": passwords[user], "temporary": False}]}
                  for user, role in roles.items()],
    }


def keycloak_resources():
    labels = {"app": "keycloak"}
    return [
        {"apiVersion": "apps/v1", "kind": "Deployment", "metadata": {"name": "keycloak", "namespace": BASYX_NAMESPACE},
         "spec": {"replicas": 1, "selector": {"matchLabels": labels}, "template": {"metadata": {"labels": labels}, "spec": {
             "containers": [{"name": "keycloak", "image": KEYCLOAK_IMAGE, "args": ["start-dev", "--import-realm"],
                 # The issuer must be the in-cluster URL the DTR validates, also for port-forwarded token requests.
                 "env": [{"name": "KC_HOSTNAME", "value": f"http://keycloak.{BASYX_NAMESPACE}.svc.cluster.local:8080"},
                         {"name": "KC_HTTP_ENABLED", "value": "true"}, {"name": "KC_HEALTH_ENABLED", "value": "true"}],
                 "ports": [{"containerPort": 8080}],
                 "readinessProbe": {"httpGet": {"path": "/health/ready", "port": 9000}, "periodSeconds": 5},
                 "resources": {"requests": {"cpu": "100m", "memory": "512Mi"}, "limits": {"memory": "1Gi"}},
                 "volumeMounts": [{"name": "realm", "mountPath": "/opt/keycloak/data/import", "readOnly": True}]}],
             "volumes": [{"name": "realm", "secret": {"secretName": "keycloak-realm"}}]}}}},
        {"apiVersion": "v1", "kind": "Service", "metadata": {"name": "keycloak", "namespace": BASYX_NAMESPACE},
         "spec": {"selector": labels, "ports": [{"name": "http", "port": 8080}]}},
    ]


class Stack:
    def __init__(self, context):
        self.context = context
        self.renderer = ["--post-renderer", sys.executable, "--post-renderer-args",
                         str(ROOT / "hack/dtr-poc/post-render.py")]

    def run(self, *args, input=None):
        command = list(map(str, args))
        flag = "--kube-context" if command[0] == "helm" else "--context"
        command = [command[0], flag, self.context, *command[1:]]
        print("+", " ".join(command), flush=True)
        subprocess.run(command, input=input, text=True, check=True)

    def apply(self, objects):
        self.run("kubectl", "apply", "-f", "-", input=yaml.safe_dump_all(objects, sort_keys=False))

    def helm(self, release, namespace, values, *extra):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml") as file:
            yaml.safe_dump(values, file, sort_keys=False)
            file.flush()
            self.run("helm", "upgrade", "--install", release, ROOT / "charts/tx-data-provider", "-n", namespace,
                     "-f", file.name, *extra, "--wait", "--timeout", "15m")

    def tractusx(self):
        self.apply([{"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": TX_NAMESPACE}}])
        self.helm(TX_RELEASE, TX_NAMESPACE, TX_VALUES)

    def exists(self, kind, name):
        command = ["kubectl", "--context", self.context, "-n", BASYX_NAMESPACE, "get", kind, name]
        return subprocess.run(command, capture_output=True).returncode == 0

    def basyx_database(self, metadata):
        if self.exists("secret", metadata["databaseSecret"]):
            # Never bootstrap or re-credential a retained database.
            print(f"Keeping existing database {metadata['postgres']}", flush=True)
            return
        namespace, _, pvc, service, statefulset, bootstrap = database_resources(metadata)
        # Dynamic provisioning instead of the Kind hostPath volume used by acceptance.py.
        pvc["spec"] = {"accessModes": ["ReadWriteOnce"], "resources": {"requests": {"storage": "1Gi"}}}
        self.apply([namespace])
        app = secrets.token_urlsafe(32)
        connection = {"host": metadata["postgres"], "port": "5432", "dbname": DATABASE, "user": DATABASE,
                      "password": app, "searchPath": DATABASE, "sslmode": "disable",
                      "jdbc-uri": f"jdbc:postgresql://{metadata['postgres']}:5432/{DATABASE}"}
        self.apply([{"apiVersion": "v1", "kind": "Secret", "type": "Opaque",
                     "metadata": {"name": name, "namespace": BASYX_NAMESPACE}, "stringData": data}
                    for name, data in ((f"{metadata['postgres']}-admin", {"password": secrets.token_urlsafe(32)}),
                                       (metadata["databaseSecret"], connection))])
        self.apply([pvc, service, statefulset])
        self.run("kubectl", "rollout", "status", "-n", BASYX_NAMESPACE, f"statefulset/{metadata['postgres']}",
                 "--timeout=300s")
        # The socket-based readiness probe also passes for initdb's temporary server; wait for TCP.
        probe = ["kubectl", "--context", self.context, "-n", BASYX_NAMESPACE, "exec", f"{metadata['postgres']}-0",
                 "--", "pg_isready", "-h", "127.0.0.1", "-U", "postgres"]
        deadline = time.monotonic() + 120
        while subprocess.run(probe, capture_output=True).returncode:
            if time.monotonic() > deadline:
                raise RuntimeError("PostgreSQL did not accept TCP connections")
            time.sleep(2)
        self.apply([bootstrap])
        self.run("kubectl", "wait", "-n", BASYX_NAMESPACE, "--for=condition=Complete",
                 f"job/{metadata['postgres']}-bootstrap", "--timeout=180s")

    def keycloak(self):
        if self.exists("secret", "keycloak-test-users"):
            print("Keeping existing Keycloak test realm", flush=True)
            return
        passwords = {user: secrets.token_urlsafe(24) for user in ("provider", "edc-dtr-reader")}
        self.apply([{"apiVersion": "v1", "kind": "Secret", "type": "Opaque",
                     "metadata": {"name": "keycloak-realm", "namespace": BASYX_NAMESPACE},
                     "stringData": {"basyx-realm.json": json.dumps(realm(passwords))}},
                    {"apiVersion": "v1", "kind": "Secret", "type": "Opaque",
                     "metadata": {"name": "keycloak-test-users", "namespace": BASYX_NAMESPACE},
                     "stringData": passwords}])
        self.apply(keycloak_resources())
        self.run("kubectl", "rollout", "restart", "-n", BASYX_NAMESPACE, "deployment/keycloak")
        self.run("kubectl", "rollout", "status", "-n", BASYX_NAMESPACE, "deployment/keycloak", "--timeout=300s")

    def basyx(self, abac):
        values, metadata = basyx_values(abac)
        self.basyx_database(metadata)
        if abac:
            self.keycloak()
        self.helm(BASYX_RELEASE, BASYX_NAMESPACE, values, *self.renderer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True, help="Explicit kube context of a local test cluster")
    parser.add_argument("--abac", action="store_true", help="Also deploy Keycloak and enable Tractus-X style ABAC")
    parser.add_argument("--only", choices=("tractusx", "basyx"), help="Install only one side")
    args = parser.parse_args()
    stack = Stack(args.context)
    if args.only != "basyx":
        stack.tractusx()
    if args.only != "tractusx":
        stack.basyx(args.abac)


if __name__ == "__main__":
    main()
