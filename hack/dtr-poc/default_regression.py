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
"""Compare the default provider to a pinned upstream main source."""
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

import yaml

BASELINE = "fe1d0cc9d8326cc68dbd6f56433d1baa403d8ebc"
RANDOM_PATHS = {
    "/ConfigMap/basyx-dtr-poc-tx-data-provider-vault-edc-configmap/data/aes-secret.json",
    "/Secret/basyx-dtr-poc-connector-postgresql/data/postgres-password",
    "/Secret/dtr-postgresql/data/postgres-password",
}


def differences(before, after, path=""):
    if type(before) is not type(after):
        return [path]
    if isinstance(before, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            result += ([path + "/" + key] if key not in before or key not in after
                       else differences(before[key], after[key], path + "/" + key))
        return result
    if isinstance(before, list):
        if len(before) != len(after):
            return [path + "/length"]
        return [p for i, (b, a) in enumerate(zip(before, after))
                for p in differences(b, a, path + "/" + str(i))]
    return [] if before == after else [path]


def verify(root, scratch, run):
    archive = subprocess.check_output(["git", "-C", str(root), "archive", BASELINE,
                                       "charts/tx-data-provider"])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(scratch, filter="data")
    chart = scratch / "charts/tx-data-provider"
    before_chart = yaml.safe_load((chart / "Chart.yaml").read_text())
    after_chart = yaml.safe_load((root / "charts/tx-data-provider/Chart.yaml").read_text())
    deps = before_chart["dependencies"]
    (chart / "charts").mkdir()
    for dependency in deps:
        package = root / "charts/tx-data-provider/charts" / f"{dependency['name']}-{dependency['version']}.tgz"
        shutil.copy2(package, chart / "charts" / package.name)
    outputs = []
    for current in (chart, root / "charts/tx-data-provider"):
        text = run("helm", "template", "basyx-dtr-poc", str(current), "-n", "umbrella-basyx-poc", quiet=True)
        outputs.append({f"{o['kind']}/{o['metadata']['name']}": o
                        for o in yaml.safe_load_all(text) if o})
    # A chart version bump changes only the default Vault hook's chart labels.
    # Validate their exact values instead of ignoring label differences.
    version_labels = []
    for key, before in outputs[0].items():
        if before["kind"] != "Job" or key not in outputs[1]:
            continue
        after = outputs[1][key]
        for path in (("metadata", "labels"), ("spec", "template", "metadata", "labels")):
            before_labels, after_labels = before, after
            for part in path:
                before_labels = before_labels.get(part, {})
                after_labels = after_labels.get(part, {})
            old = f"tx-data-provider-{before_chart['version']}"
            new = f"tx-data-provider-{after_chart['version']}"
            if before_labels.get("helm.sh/chart") == old:
                assert after_labels.get("helm.sh/chart") == new, "Unexpected chart version label"
                before_labels["helm.sh/chart"] = new
                version_labels.append(key + "/" + "/".join(path) + "/helm.sh/chart")
    assert len(version_labels) == 2, "Expected exactly two provider hook chart labels"
    changes = set(differences(*outputs))
    assert changes <= RANDOM_PATHS, "Default Tractus-X provider changed: " + json.dumps(sorted(changes - RANDOM_PATHS))
    assert outputs[0].keys() == outputs[1].keys()
    assert any(key.startswith("Deployment/") and "digital-twin-registry" in key for key in outputs[1])
    assert not any("basyx" in key and "basyx-dtr-poc" not in key for key in outputs[1])
    return {"result": "PASS", "upstreamCommit": BASELINE, "resourceCount": len(outputs[0]),
            "allowedRandomDifferences": sorted(changes), "validatedChartVersionLabels": version_labels}
