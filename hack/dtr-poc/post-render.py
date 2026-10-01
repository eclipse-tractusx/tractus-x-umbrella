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
"""Filter the unused TLS Issuer emitted by official BaSyx chart 3.15.0."""
import sys
import yaml

for obj in yaml.safe_load_all(sys.stdin):
    if not obj:
        continue
    if obj["kind"] == "Issuer" and obj["metadata"]["name"] == "internal-issuer":
        continue
    sys.stdout.write("---\n" + yaml.safe_dump(obj, sort_keys=False))
