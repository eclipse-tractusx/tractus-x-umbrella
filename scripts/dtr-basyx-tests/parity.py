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
"""Send identical requests to the stacks from local_stack.py and record both responses.

registry:   46 registry calls against Tractus-X DTR and BaSyx DTR (ABAC disabled).
submodel:   SAMM test payloads through simple-data-backend and the BaSyx Submodel Repository.
visibility: Edc-Bpn visibility against BaSyx DTR with ABAC (local_stack.py --abac).
This is a comparison report, not a pass/fail gate; differences are expected.
"""
import argparse
import base64
import collections
import contextlib
import json
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from local_stack import BASYX_NAMESPACE, TX_NAMESPACE
from tenant_profile import ROOT

OWNER = "default-tenant"  # Tractus-X REGISTRY_IDM_OWNING_TENANT_ID default
BPN_A, BPN_B = "BPNL00000003AYRE", "BPNL00000003AZQP"
TESTDATA = ROOT / "charts/tx-data-provider/resources/Testdata_AsBuilt-combustion.json"
PUBLIC = {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": "PUBLIC_READABLE"}]}


def b64(value):
    return base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")


def asset_ids(*pairs):
    return [b64(json.dumps({"name": name, "value": value})) for name, value in pairs]


def request(base, method, path, body=None, bpn=None, token=None, params=None):
    url = base + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    headers = {"Content-Type": "application/json"}
    if bpn:
        headers["Edc-Bpn"] = bpn
    if token:
        headers["Authorization"] = "Bearer " + token
    data = json.dumps(body).encode() if body is not None else None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        response = opener.open(urllib.request.Request(url, data, headers, method=method), timeout=30)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        raw, status = response.read(), response.code
    try:
        return status, json.loads(raw) if raw else None
    except ValueError:
        return status, raw.decode(errors="replace")


@contextlib.contextmanager
def forward(context, namespace, service):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    process = subprocess.Popen([shutil.which("kubectl"), "--context", context, "-n", namespace, "port-forward",
                                "--address=127.0.0.1", f"service/{service}", f"{port}:8080"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
                break
            except OSError:
                time.sleep(0.3)
        else:
            raise RuntimeError(f"Port forwarding to {namespace}/{service} timed out")
        yield f"http://127.0.0.1:{port}"
    finally:
        process.terminate()
        process.wait(timeout=10)


def submodel_descriptor(token, short, semantic):
    sid = f"urn:uuid:sm-{short}-{token}"
    return {"id": sid, "idShort": short,
            "semanticId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": semantic}]},
            "endpoints": [{"interface": "SUBMODEL-3.0", "protocolInformation": {
                "href": f"https://edc.provider.invalid/api/public/{sid}", "endpointProtocol": "HTTP",
                "endpointProtocolVersion": ["1.1"], "subprotocol": "DSP",
                "subprotocolBody": "id=asset-1;dspEndpoint=https://edc.provider.invalid/api/v1/dsp",
                "subprotocolBodyEncoding": "plain",
                "securityAttributes": [{"type": "NONE", "key": "NONE", "value": "NONE"}]}}]}


def shell(token):
    restricted = {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": BPN_A}]}
    return {"id": f"urn:uuid:{token}", "idShort": "VehicleCombustion", "assetKind": "Instance", "assetType": "Vehicle",
            "globalAssetId": f"urn:uuid:global-{token}",
            "description": [{"language": "en", "text": "parity test twin"}],
            "specificAssetIds": [
                {"name": "manufacturerId", "value": BPN_A, "externalSubjectId": PUBLIC},
                {"name": "manufacturerPartId", "value": f"MPI-{token}", "externalSubjectId": PUBLIC},
                {"name": "digitalTwinType", "value": "PartInstance", "externalSubjectId": PUBLIC},
                {"name": "partInstanceId", "value": f"PIN-{token}", "externalSubjectId": restricted}],
            "submodelDescriptors": [submodel_descriptor(token, "SerialPart",
                                                        "urn:samm:io.catenax.serial_part:3.0.0#SerialPart")]}


def view(status, body):
    """Compact, comparable projection of one response."""
    if isinstance(body, dict) and ("specificAssetIds" in body or "submodelDescriptors" in body):
        fields = sorted(k for k, v in body.items() if v not in ([], None)
                        and k not in ("createdAt", "id", "specificAssetIds", "submodelDescriptors"))
        ids = sorted(s["name"] for s in body.get("specificAssetIds", []))
        return f"{status} ids=[{','.join(ids)}] fields=[{','.join(fields)}]"
    if isinstance(body, dict) and ("result" in body or "paging_metadata" in body):
        return f"{status} result={len(body.get('result', []))}" + ("" if "result" in body else " (no result key)")
    if isinstance(body, list) and body and all(isinstance(x, dict) and "name" in x for x in body):
        return f"{status} links=[{','.join(sorted(x['name'] for x in body))}]"
    if isinstance(body, list) and body and isinstance(body[0], dict) and "correlationId" in body[0]:
        return f"{status} error[]"
    if isinstance(body, dict) and ("messages" in body or "detail" in body):
        return f"{status} error{{}}"
    return f"{status} {json.dumps(body)[:60]}"


def registry_steps(t):
    s, sid = shell(t), b64(f"urn:uuid:{t}")
    sm = submodel_descriptor(t, "SingleLevelBomAsBuilt",
                             "urn:samm:io.catenax.single_level_bom_as_built:3.0.0#SingleLevelBomAsBuilt")
    smid = b64(sm["id"])
    changed_sm, changed = dict(sm, idShort="SingleLevelBomAsBuiltV2"), dict(s, idShort="VehicleCombustionUpdated")
    link = [{"name": "vanNumber", "value": f"VAN-{t}", "externalSubjectId": {
        "type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": BPN_A}]}}]
    lookup = lambda *pairs: {"assetIds": asset_ids(*pairs)}
    return [
        ("description", "GET", "/description", None, OWNER, None),
        ("create shell", "POST", "/shell-descriptors", s, OWNER, None),
        ("create duplicate shell", "POST", "/shell-descriptors", s, OWNER, None),
        ("get shell (owner)", "GET", f"/shell-descriptors/{sid}", None, OWNER, None),
        ("get shell (no Edc-Bpn)", "GET", f"/shell-descriptors/{sid}", None, None, None),
        ("get shell (BPN A)", "GET", f"/shell-descriptors/{sid}", None, BPN_A, None),
        ("get shell (BPN B)", "GET", f"/shell-descriptors/{sid}", None, BPN_B, None),
        ("list limit=1", "GET", "/shell-descriptors", None, OWNER, {"limit": 1}),
        ("list assetKind=Instance", "GET", "/shell-descriptors", None, OWNER, {"assetKind": "Instance"}),
        ("list assetType=Vehicle", "GET", "/shell-descriptors", None, OWNER, {"assetType": b64("Vehicle")}),
        ("list (BPN B)", "GET", "/shell-descriptors", None, BPN_B, {"limit": 100}),
        ("lookup manufacturerPartId (owner)", "GET", "/lookup/shells", None, OWNER, lookup(("manufacturerPartId", f"MPI-{t}"))),
        ("lookup manufacturerPartId (BPN B)", "GET", "/lookup/shells", None, BPN_B, lookup(("manufacturerPartId", f"MPI-{t}"))),
        ("lookup partInstanceId (BPN A)", "GET", "/lookup/shells", None, BPN_A, lookup(("partInstanceId", f"PIN-{t}"))),
        ("lookup partInstanceId (BPN B)", "GET", "/lookup/shells", None, BPN_B, lookup(("partInstanceId", f"PIN-{t}"))),
        ("lookup public manufacturerId (BPN B)", "GET", "/lookup/shells", None, BPN_B, lookup(("manufacturerId", BPN_A))),
        ("lookup globalAssetId (BPN B)", "GET", "/lookup/shells", None, BPN_B, lookup(("globalAssetId", s["globalAssetId"]))),
        ("lookup two ids (BPN A)", "GET", "/lookup/shells", None, BPN_A, lookup(("manufacturerPartId", f"MPI-{t}"), ("partInstanceId", f"PIN-{t}"))),
        ("lookup no match", "GET", "/lookup/shells", None, OWNER, lookup(("manufacturerPartId", "does-not-exist"))),
        ("shellsByAssetLink (BPN A)", "POST", "/lookup/shellsByAssetLink", [{"name": "partInstanceId", "value": f"PIN-{t}"}], BPN_A, None),
        ("shellsByAssetLink (BPN B)", "POST", "/lookup/shellsByAssetLink", [{"name": "partInstanceId", "value": f"PIN-{t}"}], BPN_B, None),
        ("asset links (owner)", "GET", f"/lookup/shells/{sid}", None, OWNER, None),
        ("asset links (BPN B)", "GET", f"/lookup/shells/{sid}", None, BPN_B, None),
        ("list submodel descriptors", "GET", f"/shell-descriptors/{sid}/submodel-descriptors", None, OWNER, None),
        ("create submodel descriptor", "POST", f"/shell-descriptors/{sid}/submodel-descriptors", sm, OWNER, None),
        ("create duplicate submodel descriptor", "POST", f"/shell-descriptors/{sid}/submodel-descriptors", sm, OWNER, None),
        ("get submodel descriptor", "GET", f"/shell-descriptors/{sid}/submodel-descriptors/{smid}", None, OWNER, None),
        ("put submodel descriptor", "PUT", f"/shell-descriptors/{sid}/submodel-descriptors/{smid}", changed_sm, OWNER, None),
        ("get submodel descriptor after put", "GET", f"/shell-descriptors/{sid}/submodel-descriptors/{smid}", None, OWNER, None),
        ("delete submodel descriptor", "DELETE", f"/shell-descriptors/{sid}/submodel-descriptors/{smid}", None, OWNER, None),
        ("get deleted submodel descriptor", "GET", f"/shell-descriptors/{sid}/submodel-descriptors/{smid}", None, OWNER, None),
        ("put shell", "PUT", f"/shell-descriptors/{sid}", changed, OWNER, None),
        ("get shell after put", "GET", f"/shell-descriptors/{sid}", None, OWNER, None),
        ("add asset link", "POST", f"/lookup/shells/{sid}", link, OWNER, None),
        ("asset links after add", "GET", f"/lookup/shells/{sid}", None, OWNER, None),
        ("lookup added link (BPN A)", "GET", "/lookup/shells", None, BPN_A, lookup(("vanNumber", f"VAN-{t}"))),
        ("get shell after link add", "GET", f"/shell-descriptors/{sid}", None, OWNER, None),
        ("get unknown shell", "GET", f"/shell-descriptors/{b64('urn:uuid:nope')}", None, OWNER, None),
        ("get shell non-base64 id", "GET", "/shell-descriptors/%25%25%25", None, OWNER, None),
        ("create without id", "POST", "/shell-descriptors", {"idShort": "x"}, OWNER, None),
        ("create invalid assetKind", "POST", "/shell-descriptors", {"id": f"urn:uuid:bad-{t}", "assetKind": "BAD"}, OWNER, None),
        ("list limit=0", "GET", "/shell-descriptors", None, OWNER, {"limit": 0}),
        ("list invalid cursor", "GET", "/shell-descriptors", None, OWNER, {"cursor": "garbage"}),
        ("delete shell", "DELETE", f"/shell-descriptors/{sid}", None, OWNER, None),
        ("get deleted shell", "GET", f"/shell-descriptors/{sid}", None, OWNER, None),
        ("lookup deleted shell", "GET", "/lookup/shells", None, OWNER, lookup(("manufacturerPartId", f"MPI-{t}"))),
    ]


def compare(rows, out, name):
    out.joinpath(f"{name}.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        mark = "SAME" if row["same"] else "DIFF"
        print(f"{mark} {row['step'][:46]:46} TX {row['tractusx'][:60]:60} | BX {row['basyx'][:60]}")
    same = sum(r["same"] for r in rows)
    status = sum(r["tractusx"].split()[0] == r["basyx"].split()[0] for r in rows)
    print(f"{name}: {len(rows)} calls, same status {status}, same projection {same}")


def registry(context, out):
    rows, token = [], uuid.uuid4().hex[:12]
    with forward(context, TX_NAMESPACE, "txdtr-digital-twin-registry") as tx, \
            forward(context, BASYX_NAMESPACE, "basyx-poc-digital-twin-registry") as bx:
        results = {}
        for side, base in (("tractusx", tx + "/api/v3"), ("basyx", bx + "/digital-twin-registry")):
            results[side] = [request(base, m, p, body, bpn, None, params)
                             for _, m, p, body, bpn, params in registry_steps(token)]
    for i, (step, method, path, body, bpn, params) in enumerate(registry_steps(token)):
        a, b = results["tractusx"][i], results["basyx"][i]
        rows.append({"step": step, "request": {"method": method, "path": path, "edcBpn": bpn, "params": params,
                                               "body": body},
                     "tractusx": view(*a), "basyx": view(*b), "same": view(*a) == view(*b),
                     "tractusxResponse": {"status": a[0], "body": a[1]}, "basyxResponse": {"status": b[0], "body": b[1]}})
    compare(rows, out, "registry-parity")


def element(key, value, in_list=False):
    """Convert one SAMM JSON value into an AAS SubmodelElement."""
    result = {} if in_list else {"idShort": key}
    if isinstance(value, dict):
        result.update(modelType="SubmodelElementCollection", value=[element(k, v) for k, v in value.items()])
    elif isinstance(value, list):
        kinds = {type(v) for v in value}
        result["modelType"] = "SubmodelElementList"
        if value and kinds <= {dict}:
            result["typeValueListElement"] = "SubmodelElementCollection"
        elif value and kinds <= {list}:
            result["typeValueListElement"] = "SubmodelElementList"
        else:
            result.update(typeValueListElement="Property", valueTypeListElement=xs(value[0]) if value else "xs:string")
        result["value"] = [element(None, v, True) for v in value]
    else:
        result.update(modelType="Property", valueType=xs(value))
        if value is not None:
            result["value"] = str(value).lower() if isinstance(value, bool) else str(value)
    return result


def xs(value):
    # Strings, including timestamps, stay xs:string so they round-trip byte for byte.
    return {bool: "xs:boolean", int: "xs:long", float: "xs:double"}.get(type(value), "xs:string")


def aas_submodel(identifier, semantic, payload):
    return {"modelType": "Submodel", "id": identifier, "kind": "Instance", "idShort": semantic.split("#")[-1],
            "semanticId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": semantic}]},
            "submodelElements": [element(k, v) for k, v in payload.items()]}


def changed_leaves(expected, actual, counter):
    if isinstance(expected, dict):
        for key, value in expected.items():
            changed_leaves(value, actual.get(key) if isinstance(actual, dict) else None, counter)
    elif isinstance(expected, list):
        for i, value in enumerate(expected):
            changed_leaves(value, actual[i] if isinstance(actual, list) and i < len(actual) else None, counter)
    elif expected != actual:
        counter[f"{type(expected).__name__}->{type(actual).__name__}"] += 1


def submodel(context, out):
    data = json.loads(TESTDATA.read_text(encoding="utf-8"))["https://catenax.io/schema/TestDataContainer/1.0.0"]
    payloads = [(k, v[0]) for twin in data for k, v in twin.items()
                if k.startswith("urn:samm:") and isinstance(v, list) and v and isinstance(v[0], dict)]
    leaves, aspects, results = collections.Counter(), collections.defaultdict(lambda: [0, 0, 0]), []
    with forward(context, TX_NAMESPACE, "txdtr-simple-data-backend") as backend, \
            forward(context, BASYX_NAMESPACE, "basyx-poc-submodel-repository") as basyx:
        repository = basyx + "/submodel-repo"
        raw = request(repository, "POST", "/submodels", payloads[0][1])
        for semantic, payload in payloads:
            identifier = f"urn:uuid:{uuid.uuid4()}"
            request(backend, "POST", f"/{identifier}", payload)
            simple = request(backend, "GET", f"/{identifier}/$value")
            created = request(repository, "POST", "/submodels", aas_submodel(identifier, semantic, payload))
            value = request(repository, "GET", f"/submodels/{b64(identifier)}/$value")
            counter = collections.Counter()
            changed_leaves(payload, value[1], counter)
            leaves.update(counter)
            aspect = aspects[semantic.split("#")[-1]]
            aspect[0] += 1
            aspect[1] += simple[1] == payload
            aspect[2] += value[1] == payload
            results.append({"semanticId": semantic, "simpleBackendExact": simple[1] == payload,
                            "basyxCreate": created[0], "basyxValue": value[0], "basyxExact": value[1] == payload,
                            "changedLeaves": dict(counter)})
        missing = (request(backend, "GET", "/urn:uuid:missing/$value"),
                   request(repository, "GET", f"/submodels/{b64('urn:uuid:missing')}/$value"))
    report = {"rawSammPostToBasyx": {"status": raw[0], "body": raw[1]},
              "aspects": {k: {"payloads": v[0], "simpleBackendExact": v[1], "basyxExact": v[2]} for k, v in aspects.items()},
              "changedLeaves": dict(leaves), "notFound": {"simpleBackend": missing[0], "basyx": missing[1]},
              "results": results}
    out.joinpath("submodel-parity.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("BaSyx POST raw SAMM JSON:", raw[0], json.dumps(raw[1])[:120])
    for name, (count, simple, exact) in sorted(aspects.items()):
        print(f"{name:40} payloads {count:3}  simple-data-backend exact {simple:3}  BaSyx $value exact {exact:3}")
    print("Changed leaf values in BaSyx $value:", dict(leaves))


def secret_value(context, name, key):
    raw = subprocess.run(["kubectl", "--context", context, "-n", BASYX_NAMESPACE, "get", "secret", name,
                          "-o", f"jsonpath={{.data.{key}}}"], capture_output=True, text=True, check=True).stdout
    return base64.b64decode(raw).decode()


def token_for(keycloak, context, user):
    form = urllib.parse.urlencode({"grant_type": "password", "client_id": "basyx-ui", "username": user,
                                   "password": secret_value(context, "keycloak-test-users", user)}).encode()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f"{keycloak}/realms/basyx/protocol/openid-connect/token", form, timeout=30) as response:
        return json.loads(response.read())["access_token"]


def visibility(context, out):
    t = uuid.uuid4().hex[:12]
    s, sid = shell(t), b64(f"urn:uuid:{t}")
    lookup = lambda *pairs: {"assetIds": asset_ids(*pairs)}
    pin_link = [{"name": "partInstanceId", "value": f"PIN-{t}"}]
    # step, method, path, body, Tractus-X Edc-Bpn, BaSyx Edc-Bpn, BaSyx identity, compare with Tractus-X
    steps = [
        ("create without token", "POST", "/shell-descriptors", s, None, None, None, False),
        ("create as EDC reader", "POST", "/shell-descriptors", s, None, None, "edc-dtr-reader", False),
        ("create as provider", "POST", "/shell-descriptors", s, OWNER, None, "provider", True),
        ("read without token", "GET", f"/shell-descriptors/{sid}", None, None, None, None, False),
        ("read as provider (no Edc-Bpn)", "GET", f"/shell-descriptors/{sid}", None, OWNER, None, "provider", True),
        ("read as owner", "GET", f"/shell-descriptors/{sid}", None, OWNER, OWNER, "edc-dtr-reader", True),
        ("read as BPN A", "GET", f"/shell-descriptors/{sid}", None, BPN_A, BPN_A, "edc-dtr-reader", True),
        ("read as BPN B", "GET", f"/shell-descriptors/{sid}", None, BPN_B, BPN_B, "edc-dtr-reader", True),
        ("read with no Edc-Bpn", "GET", f"/shell-descriptors/{sid}", None, None, None, "edc-dtr-reader", True),
        ("list as BPN B", "GET", "/shell-descriptors", None, BPN_B, BPN_B, "edc-dtr-reader", True),
        ("lookup manufacturerPartId as BPN B", "GET", "/lookup/shells", lookup(("manufacturerPartId", f"MPI-{t}")), BPN_B, BPN_B, "edc-dtr-reader", True),
        ("lookup partInstanceId as BPN A", "GET", "/lookup/shells", lookup(("partInstanceId", f"PIN-{t}")), BPN_A, BPN_A, "edc-dtr-reader", True),
        ("lookup partInstanceId as BPN B", "GET", "/lookup/shells", lookup(("partInstanceId", f"PIN-{t}")), BPN_B, BPN_B, "edc-dtr-reader", True),
        ("lookup public manufacturerId as BPN B", "GET", "/lookup/shells", lookup(("manufacturerId", BPN_A)), BPN_B, BPN_B, "edc-dtr-reader", True),
        ("lookup globalAssetId as BPN B", "GET", "/lookup/shells", lookup(("globalAssetId", s["globalAssetId"])), BPN_B, BPN_B, "edc-dtr-reader", True),
        ("lookup manufacturerPartId, no Edc-Bpn", "GET", "/lookup/shells", lookup(("manufacturerPartId", f"MPI-{t}")), None, None, "edc-dtr-reader", True),
        ("shellsByAssetLink as BPN A", "POST", "/lookup/shellsByAssetLink", pin_link, BPN_A, BPN_A, "edc-dtr-reader", True),
        ("shellsByAssetLink as BPN B", "POST", "/lookup/shellsByAssetLink", pin_link, BPN_B, BPN_B, "edc-dtr-reader", True),
        ("asset links as owner", "GET", f"/lookup/shells/{sid}", None, OWNER, OWNER, "edc-dtr-reader", True),
        ("asset links as BPN B", "GET", f"/lookup/shells/{sid}", None, BPN_B, BPN_B, "edc-dtr-reader", True),
        ("submodel descriptors as BPN B", "GET", f"/shell-descriptors/{sid}/submodel-descriptors", None, BPN_B, BPN_B, "edc-dtr-reader", True),
        ("delete as EDC reader", "DELETE", f"/shell-descriptors/{sid}", None, None, None, "edc-dtr-reader", False),
        ("delete as provider", "DELETE", f"/shell-descriptors/{sid}", None, OWNER, None, "provider", True),
    ]
    rows = []
    with forward(context, TX_NAMESPACE, "txdtr-digital-twin-registry") as tx, \
            forward(context, BASYX_NAMESPACE, "basyx-poc-digital-twin-registry") as bx, \
            forward(context, BASYX_NAMESPACE, "keycloak") as keycloak:
        tokens = {user: token_for(keycloak, context, user) for user in ("provider", "edc-dtr-reader")}
        for step, method, path, body, tx_bpn, bx_bpn, user, comparable in steps:
            params = body if method == "GET" and body else None
            payload = None if params else body
            a = request(tx + "/api/v3", method, path, payload, tx_bpn, None, params) if comparable else None
            b = request(bx + "/digital-twin-registry", method, path, payload, bx_bpn, tokens.get(user), params)
            rows.append({"step": step, "request": {"method": method, "path": path, "edcBpn": bx_bpn, "identity": user},
                         "tractusx": view(*a) if a else "n/a", "basyx": view(*b),
                         "same": bool(a) and view(*a) == view(*b),
                         "tractusxResponse": a and {"status": a[0], "body": a[1]},
                         "basyxResponse": {"status": b[0], "body": b[1]}})
    compare(rows, out, "visibility-parity")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("suite", choices=("registry", "submodel", "visibility"))
    parser.add_argument("--context", required=True, help="Kube context used with local_stack.py")
    parser.add_argument("--out", required=True, type=Path, help="Directory for the JSON results")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    {"registry": registry, "submodel": submodel, "visibility": visibility}[args.suite](args.context, args.out)


if __name__ == "__main__":
    main()
