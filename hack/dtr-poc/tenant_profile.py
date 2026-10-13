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
"""Render credential-free values for one independent BaSyx tenant instance."""
import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def safe_name(value, limit):
    if len(value) > limit or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", value):
        raise ValueError(f"Expected a DNS label of at most {limit} characters")
    return value


def profile(namespace, release, tenant):
    """Only configuration generation; never connects to Kubernetes or a database."""
    safe_name(namespace, 63)
    safe_name(release, 30)
    safe_name(tenant, 24)
    # Keep the longest upstream name (<fullname>-digital-twin-registry) <= 63.
    fullname = safe_name(f"{release}-{tenant}", 41)
    values = yaml.safe_load((ROOT / "charts/tx-data-provider/values-basyx-poc.yaml").read_text())
    service = f"{fullname}-digital-twin-registry"
    values["registryUrl"] = f"http://{service}.{namespace}.svc.cluster.local:8080/digital-twin-registry"
    values["digital-twin-basyx-bundle"]["basyx"] = {
        "instanceName": tenant,
        "fullnameOverride": fullname,
        "host": f"{tenant}.invalid",
        "database": {"type": "external", "existingSecret": f"{fullname}-database"},
        "digitalTwinRegistry": {"serviceAccount": {"name": f"{fullname}-dtr"}},
    }
    return values, {"namespace": namespace, "release": release, "tenant": tenant,
                    "fullname": fullname, "service": service,
                    "databaseSecret": f"{fullname}-database", "postgres": f"{fullname}-postgres",
                    "apiBase": values["registryUrl"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--release", required=True)
    parser.add_argument("--tenant", required=True)
    args = parser.parse_args()
    print(yaml.safe_dump(profile(args.namespace, args.release, args.tenant)[0], sort_keys=False), end="")
