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
"""Use fresh synthetic descriptors; never read a production endpoint."""
import base64
import copy
import json
import urllib.error
import urllib.request


def encoded(identifier):
    return base64.urlsafe_b64encode(identifier.encode()).decode().rstrip("=")


class Api:
    def __init__(self, base, events):
        self.base, self.events = base, events
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def call(self, method, path, data=None, expected=200, bpn="BPNL000000POC001"):
        request = urllib.request.Request(self.base + path, method=method,
            data=json.dumps(data).encode() if data is not None else None,
            headers={"Content-Type": "application/json", "Edc-Bpn": bpn})
        try:
            response = self.opener.open(request, timeout=30)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            raw, status = response.read(2_000_001), response.code
        if len(raw) > 2_000_000:
            raise AssertionError("Oversized synthetic API response")
        try:
            value = json.loads(raw) if raw else None
        except ValueError:
            value = raw.decode(errors="replace")
        self.events.append({"method": method, "path": path, "request": data,
                            "status": status, "response": value})
        assert status == expected, (method, path, status, expected)
        return value


def fixture(token, tenant):
    return {"id": f"urn:basyx:poc:tenant:{token}", "idShort": tenant,
        "assetKind": "Instance", "globalAssetId": f"urn:basyx:poc:asset:{token}",
        "specificAssetIds": [{"name": "serialNumber", "value": token,
            "externalSubjectId": {"type": "ExternalReference",
                "keys": [{"type": "GlobalReference", "value": "PUBLIC_READABLE"}]}}],
        "submodelDescriptors": [{"id": f"urn:basyx:poc:submodel:{token}", "idShort": "Part",
            "semanticId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference",
                "value": "urn:samm:io.catenax.serial_part:3.0.0#SerialPart"}]},
            "endpoints": [{"interface": "SUBMODEL-3.0", "protocolInformation": {
                "href": "https://data.invalid/submodels/" + encoded(token),
                "endpointProtocol": "HTTP", "endpointProtocolVersion": ["1.1"],
                "subprotocol": "DSP", "subprotocolBody": "id=poc;dspEndpoint=https://dsp.invalid/api",
                "subprotocolBodyEncoding": "plain",
                "securityAttributes": [{"type": "NONE", "key": "NONE", "value": "NONE"}]}}]}]}


def assert_contains(actual, expected):
    if isinstance(expected, dict):
        for key, value in expected.items():
            assert key in actual, key
            assert_contains(actual[key], value)
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for item, value in zip(actual, expected):
            assert_contains(item, value)
    else:
        assert actual == expected, (actual, expected)


def crud(api, descriptor):
    api.call("GET", "/health")
    api.call("POST", "/shell-descriptors", descriptor, 201)
    path = "/shell-descriptors/" + encoded(descriptor["id"])
    assert_contains(api.call("GET", path), descriptor)
    changed = copy.deepcopy(descriptor)
    changed["idShort"] += "Updated"
    api.call("PUT", path, changed, 204)
    actual = api.call("GET", path)
    assert_contains(actual, changed)
    links = [{"name": "globalAssetId", "value": descriptor["globalAssetId"]}]
    assert descriptor["id"] in api.call("POST", "/lookup/shellsByAssetLink", links)["result"]
    links = [{"name": "serialNumber", "value": descriptor["specificAssetIds"][0]["value"]}]
    assert descriptor["id"] in api.call("POST", "/lookup/shellsByAssetLink", links)["result"]
    transient = copy.deepcopy(descriptor)
    transient["id"] += ":deleted"
    api.call("POST", "/shell-descriptors", transient, 201)
    api.call("DELETE", "/shell-descriptors/" + encoded(transient["id"]), expected=204)
    api.call("GET", "/shell-descriptors/" + encoded(transient["id"]), expected=404)
    api.call("POST", "/shell-descriptors", {"id": descriptor["id"] + ":bad", "assetKind": "BAD"}, 400)
    return actual


def read_persisted(api, actual):
    assert api.call("GET", "/shell-descriptors/" + encoded(actual["id"])) == actual
    links = [{"name": "globalAssetId", "value": actual["globalAssetId"]}]
    assert actual["id"] in api.call("POST", "/lookup/shellsByAssetLink", links)["result"]
