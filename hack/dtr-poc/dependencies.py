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
"""Resolve only the provider's dependency tree, from leaves to parent."""
import hashlib
import subprocess
from tenant_profile import ROOT

for name, url in {
    "basyx": "https://eclipse-basyx.github.io/charts",
    "tractusx": "https://eclipse-tractusx.github.io/charts/dev",
    "bitnami": "https://charts.bitnami.com/bitnami",
    "hashicorp": "https://helm.releases.hashicorp.com",
}.items():
    subprocess.run(["helm", "repo", "add", name, url, "--force-update"], check=True)
subprocess.run(["helm", "repo", "update"], check=True)
for name in ["digital-twin-basyx-bundle", "digital-twin-bundle", "data-persistence-layer-bundle",
             "dataspace-connector-bundle", "tx-data-provider"]:
    subprocess.run(["helm", "dependency", "update", str(ROOT / "charts" / name), "--skip-refresh"], check=True)
package = ROOT / "charts/digital-twin-basyx-bundle/charts/basyx-3.15.0.tgz"
assert hashlib.sha256(package.read_bytes()).hexdigest() == "a04f061a241cc2d8c6d8c530369f5e33694881aa222a408c11d75dac6a5a9ffd", "BaSyx chart checksum changed"
