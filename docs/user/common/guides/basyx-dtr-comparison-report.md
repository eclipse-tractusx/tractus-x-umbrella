<!-- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# BaSyx DTR and Submodel Repository: comparison report

This report compares the optional BaSyx bundle
(`charts/digital-twin-basyx-bundle`) with the components the umbrella uses
today. It answers three questions:

1. Does the BaSyx Digital Twin Registry behave like the Tractus-X Digital
   Twin Registry?
2. Can BaSyx ABAC filter data by `Edc-Bpn` the same way the Tractus-X DTR
   does, and how do you configure it?
3. Can the BaSyx Submodel Repository replace `simple-data-backend` as the
   submodel data service?

Every request and response below was captured from a local run on
2026-10-26, on the branch of PR #441 after merging `main` (Tractus-X DTR
0.12.0). The two stacks received identical requests. The scripts that install
both stacks and send the requests are in [`hack/dtr-poc/`](../../../../hack/dtr-poc/README.md#compare-with-the-tractus-x-dtr);
see [Section 10](#10-reproduce). For how to install the
bundle, see [Evaluate an optional BaSyx DTR](basyx-dtr-poc.md).

## Summary

| Question | Result |
|---|---|
| Registry API (CRUD, paging, lookup, submodel descriptors) | **Compatible for the main flows.** 42 of 46 calls returned the same HTTP status. Section 3 compares every endpoint. Section 4 shows the details. |
| `Edc-Bpn` visibility, as the bundle ships it (`abac.enabled: false`) | **Not equivalent. This blocks a migration.** BaSyx returns every `specificAssetId` to every caller. It also finds twins by restricted asset IDs for any BPN. |
| `Edc-Bpn` visibility with the ABAC rules in [Section 6](#6-configure-abac-for-tractus-x-style-visibility) | **Equivalent for reads and lookups.** 16 of 19 checks returned the same result. Two of the three remaining differences are built into BaSyx and cannot be changed with rules. |
| Error responses | **Different.** Tractus-X returns `{"messages":[…]}`. BaSyx returns a bare array `[{code, correlationId, …}]`. |
| Submodel Repository as the data backend | **Works, but needs migration work.** The upload format changes from raw SAMM JSON to an AAS `Submodel`. URLs must use Base64URL-encoded IDs. `$value` returns **every number and boolean as a JSON string**. 56 of 112 test payloads did not round-trip exactly. |
| Running on Apple Silicon (arm64) | The bundle pins **amd64-only** image digests. The multi-arch index digests of the same `1.1.0` release work natively. |

## 1. Test setup

| Item | Tractus-X stack (namespace `txdtr`) | BaSyx stack (namespace `basyx`) |
|---|---|---|
| Chart | `tx-data-provider` 0.6.2 (`digital-twin-bundle` 1.4.0, `data-persistence-layer-bundle` 1.0.0) | `tx-data-provider` 0.6.2 + `values-basyx-poc.yaml` (`digital-twin-basyx-bundle` 0.1.2 → `basyx` chart 3.15.0), external database profile |
| Registry | `tractusx/sldt-digital-twin-registry:0.12.0`, authentication off | `eclipsebasyx/digitaltwinregistry-go` 1.1.0. ABAC off for Sections 3 to 5; ABAC on with Keycloak 26.4 for Section 6. |
| Registry database | Bitnami PostgreSQL 15.4 (subchart) | External `postgres:18.4`, set up with `hack/dtr-poc/fixtures.py` |
| Data service | `tractusx/simple-data-backend:main` | `eclipsebasyx/submodelrepository-go` 1.1.0, added to the same BaSyx release and sharing its database |
| API base | `http://<release>-digital-twin-registry:8080/api/v3` | `http://<fullname>-digital-twin-registry:8080/digital-twin-registry` |
| Data base | `http://<release>-simple-data-backend:8080` | `http://<fullname>-submodel-repository:8080/submodel-repo` |

Environment: macOS arm64, Docker Desktop, minikube 1.34 (profile
`basyx-dtr-test`, Kubernetes 1.30.0, 4 CPU, 6 GB), Helm 3.16.4.
The EDC, IAM and wallet components were **not** deployed. All calls went
straight to the services through `kubectl port-forward`.

### Values used for the BaSyx stack

These values come from `hack/dtr-poc/tenant_profile.py --namespace basyx
--release basyx --tenant poc`, plus the overrides below:

```yaml
digital-twin-basyx-bundle:
  basyx:
    # Same 1.1.0 release: multi-arch index digests instead of amd64-only manifests
    digitalTwinRegistry:
      image:
        digest: sha256:aa8bd6fefde0dfc75a74aa7f0d3fce1cc5a5ab90f70a7824ab6ca8d56a9dfa54
    configurationService:
      image:
        digest: sha256:eb01ef0f118054ad1a3eb6081ad9997688523b0ab12d90e87c41592f50318b9d
    submodelRepository:
      enabled: true
      image:
        digest: sha256:2b5849cdf759e48cada6b3eba83f826f9117ac0371cd3b6dc8fa50552806cd2f
      ingress:
        enabled: false
      httpRoute:
        enabled: false
      environment:
        GENERAL_SUBMODELREGISTRYINTEGRATION: false   # no Submodel Registry deployed
        GENERAL_EXTERNALURL: "http://basyx-poc-submodel-repository.basyx.svc.cluster.local:8080/submodel-repo"
```

The Configuration Service job initializes the shared schema before either
Deployment starts. The Submodel Repository started against that schema with
no extra database setup. Both pods started with zero restarts.

### Values used for the Tractus-X stack

```yaml
seedTestdata: false
dataspace-connector-bundle:
  enabled: false
  tractusx-connector: { enabled: false }
  postgresql: { enabled: false }
  vault: { enabled: false }
```

### Image architecture

The bundle pins the `linux/amd64` manifests, not the multi-arch index:

| Image (1.1.0) | Digest pinned in the bundle (= amd64 entry) | Multi-arch index digest |
|---|---|---|
| `digitaltwinregistry-go` | `sha256:cc935fb6…bbc4` | `sha256:aa8bd6fe…fa54` |
| `basyxconfigurationservice-go` | `sha256:b8f863fb…5219` | `sha256:eb01ef0f…b9d` |
| `submodelrepository-go` | – | `sha256:2b5849cd…f2f` |

`tractusx/sldt-digital-twin-registry:0.12.0` is published for amd64 only. It
ran under emulation on arm64 and took about 52 s to start. All BaSyx images and
`simple-data-backend` ran natively.

## 2. Test scenarios

The registry suite sent the same 46 calls to both registries, in order. The
test shell had these four `specificAssetIds`:

| name | `externalSubjectId` |
|---|---|
| `manufacturerId` | `PUBLIC_READABLE` |
| `manufacturerPartId` | `PUBLIC_READABLE` |
| `digitalTwinType` | `PUBLIC_READABLE` |
| `partInstanceId` | `BPNL00000003AYRE` (BPN A) only |

The suite used three types of caller:

- **Owner:** `Edc-Bpn: default-tenant`, which is the Tractus-X
  `REGISTRY_IDM_OWNING_TENANT_ID`.
- **BPN A:** `Edc-Bpn: BPNL00000003AYRE`, which is allowed to see
  `partInstanceId`.
- **BPN B:** `Edc-Bpn: BPNL00000003AZQP`, which should see only public IDs. A
  separate run sent no `Edc-Bpn` header at all.

## 3. API comparison

Both registries use the same resource paths below their API base:
`/api/v3` for Tractus-X and `/digital-twin-registry` for BaSyx. The verdicts
below come from the calls in this test. Where a call was made against BaSyx
with ABAC on, that is stated.

Legend:

- ✅ **Same**: same status code and the same data.
- 🟡 **Similar**: same status code and the same data, but the response format
  differs (field order, empty arrays left out, `createdAt`, error envelope).
- 🔴 **Different**: a different status code or different data. Clients need
  changes.
- ➕ BaSyx only.
- ➖ Tractus-X only.

### 3.1 Shell descriptors

| Endpoint | Verdict | Tractus-X 0.12.0 | BaSyx 1.1.0 | What changes |
|---|---|---|---|---|
| `GET /description` | 🔴 | `200`, profiles: AAS Registry and **Discovery** SSP-001 for API 3.0 and 3.1 (IDTA URIs) | `200`, profiles: `https://basyx.org/aas/API/3/2/…Registry…/SSP-001` and IDTA `…/3/2/…Registry…/SSP-003`. **No Discovery profile** is listed. | Clients that check for an IDTA `3/0` or `3/1` registry or discovery profile will not find one. |
| `POST /shell-descriptors` | 🟡 | `201` + descriptor. Adds `displayName: []`. | `201` + descriptor. Leaves out empty arrays. | None for tolerant JSON clients. |
| `POST /shell-descriptors` (duplicate) | 🔴 | `400 {"messages":[…"does already exists"]}` | `409 [{"code":"409",…}]` | Treat `400` and `409` as "already exists". |
| `POST /shell-descriptors` (invalid body) | 🟡 | `400`, `messages[]` or RFC 7807 | `400 [{…}]` | Error parsing (Section 4.3). |
| `GET /shell-descriptors` | 🟡 | `200`, `{paging_metadata, result}` | `200`, same shape | – |
| `GET /shell-descriptors?limit=1` | 🟡 | Returns a cursor **even on the last page** | No cursor on the last page | Loop until there is no cursor. Both behave correctly with that loop. |
| `GET /shell-descriptors?cursor=<invalid>` | 🔴 | `200`: ignores the cursor | `400` | Do not send cursors you did not receive. |
| `GET /shell-descriptors?assetKind=Instance` | 🔴 | `400` | `200`, filtered | BaSyx supports this filter; Tractus-X does not. |
| `GET /shell-descriptors?assetType=<b64>` | ✅ | `200`, filtered | `200`, filtered | – |
| `GET /shell-descriptors?createdAfter=<RFC3339>` | ✅ | `200`, filtered | `200`, filtered | – |
| `GET /shell-descriptors?createdFrom=` / `updatedFrom=` | ➕ | ignored | `200`, filtered | – |
| `GET /shell-descriptors/{id}` (owner) | 🟡 | `200`, full descriptor | `200`, full descriptor | – |
| `GET /shell-descriptors/{id}` (non-owner) | 🔴 / ✅ | Filtered by `Edc-Bpn` | ABAC off: **not filtered**. ABAC on: filtered the same way. | Configure ABAC (Section 6). |
| `GET /shell-descriptors/{id}` (not found) | 🟡 | `404 {"messages":[…]}` | `404 [{…}]` | Error parsing |
| `GET /shell-descriptors/%%%` (not Base64) | 🟡 | `400` **Jetty HTML page** | `400 [{… "expected base64url"}]` | – |
| `PUT /shell-descriptors/{id}` (exists) | ✅ | `204` | `204` | – |
| `PUT /shell-descriptors/{id}` (does not exist) | 🔴 | `500 Internal Server Error` | `201`: creates the descriptor (upsert) | BaSyx supports create-or-update. |
| `DELETE /shell-descriptors/{id}` | ✅ | `204`, then `GET` returns `404` | `204`, then `GET` returns `404` | – |

### 3.2 Submodel descriptors

| Endpoint | Verdict | Tractus-X | BaSyx | What changes |
|---|---|---|---|---|
| `GET /shell-descriptors/{id}/submodel-descriptors` | ✅ | `200`, `result[1]` | `200`, `result[1]` | – |
| `POST …/submodel-descriptors` | 🟡 | `201`. Adds `description: []` and `displayName: []`. | `201`. Leaves out empty arrays. | – |
| `POST …/submodel-descriptors` (duplicate) | 🔴 | `400` | `409` | Same as for shells |
| `GET …/submodel-descriptors/{smId}` | 🟡 | `200` | `200` | – |
| `PUT …/submodel-descriptors/{smId}` | ✅ | `204` | `204` | – |
| `DELETE …/submodel-descriptors/{smId}` | ✅ | `204`, then `GET` returns `404` | `204`, then `GET` returns `404` | – |
| `POST /submodel-descriptor/authorized` | ➖ | Present: the EDC check for granular access control | **`404`, route does not exist** | Only matters if you use Tractus-X granular access control (`REGISTRY_USE_GRANULAR_ACCESS_CONTROL=true`). That mode has no BaSyx equivalent. |

### 3.3 Discovery and asset links

| Endpoint | Verdict | Tractus-X | BaSyx | What changes |
|---|---|---|---|---|
| `GET /lookup/shells?assetIds=…` (match) | ✅ | `200`, `result[1]` | `200`, `result[1]` | – |
| `GET /lookup/shells?assetIds=…` (two IDs, AND) | ✅ | `200`, `result[1]` | `200`, `result[1]` | – |
| `GET /lookup/shells?assetIds=…` (no match) | 🔴 | `{"paging_metadata":{},"result":[]}` | `{"paging_metadata":{}}`: **no `result` key** | Read `result` with a default. |
| `GET /lookup/shells?…&createdAfter=` | ✅ | filtered | filtered | – |
| `GET /lookup/shells` with a restricted ID, wrong BPN | 🔴 / ✅ | `result[0]` | ABAC off: **found**. ABAC on: `result[0]`. | Configure ABAC (Section 6). |
| `GET /lookup/shells` with a `PUBLIC_READABLE` ID of a non-wildcard type | 🔴 | `result[0]`: only the `manufacturerPartId` and `digitalTwinType` types are public | **found**, even with ABAC on | Built into BaSyx (Section 6.5). Put `PUBLIC_READABLE` only on wildcard types. |
| `GET /lookup/shells` by `globalAssetId` | ✅ | found, for any BPN | found, for any BPN | – |
| `POST /lookup/shellsByAssetLink` | ✅ / 🔴 | `200`, filtered by BPN | ABAC off: **not filtered**. ABAC on: filtered the same way. | Configure ABAC |
| `POST /lookup/shellsByAssetLink?createdAfter=` | 🔴 | parameter **ignored** | filtered | – |
| `GET /lookup/shells/{id}` (owner) | 🟡 | `200`, 4 links | `200`, 5 links: **adds `globalAssetId`** | Ignore the `globalAssetId` link. |
| `GET /lookup/shells/{id}` (non-owner) | 🔴 | `200`, only the visible links | ABAC off: all links. With the Section 6 rules: `403`. | Rules can only allow or deny this route, not filter it. Consumers rarely call this route. |
| `POST /lookup/shells/{id}` | 🟡 | `201` + the added links | `201` + the added links. **Appends** without deduplicating. | Avoid sending the same link twice. |
| `DELETE /lookup/shells/{id}` | 🟡 | `204`, then `GET` returns `200 []` | `204`, then `GET` returns `404` | Treat `404` as "no links". |

### 3.4 BaSyx-only endpoints

| Endpoint | Note |
|---|---|
| `POST /query/shell-descriptors` | AAS Query Language search. With ABAC on, it needs its own object in the rules, otherwise it returns `403`. |
| `POST`, `PUT`, `DELETE /bulk/shell-descriptors`, `GET /bulk/status/{h}`, `GET /bulk/result/{h}` | Asynchronous bulk API. Also needs its own object in the ABAC rules. |
| `POST /verify` | Checks the request against ABAC |
| `GET /health`, `/swagger`, `/api-docs/openapi.yaml` | Operations endpoints. Tractus-X uses actuator on port 4243 and its spec at `/aas-registry-openapi.yaml`. |

### 3.5 Access and headers

| Topic | Tractus-X | BaSyx | Verdict |
|---|---|---|---|
| Tenant header | `Edc-Bpn` | `Edc-Bpn`, but only used as an ABAC claim, and only when `GENERAL_ENABLECUSTOMMIDDLEWAREHEADERINJECTION=true` (chart default: `false`) | 🔴 You must configure it. |
| Owner | `Edc-Bpn` == `REGISTRY_IDM_OWNING_TENANT_ID` | An ABAC formula (Section 6) | ✅ after you configure it |
| `PUBLIC_READABLE` | Only for types in `REGISTRY_EXTERNAL_SUBJECT_ID_WILDCARD_ALLOWED_TYPES` | Any type for lookups. Reads are configurable. | 🟡 |
| Authentication | Optional OAuth2 with the roles `view_digital_twin`, `add_digital_twin`, `update_digital_twin` and `delete_digital_twin` | Optional OIDC + ABAC, with the same role names as claims | ✅ |
| Error envelope | `{"messages":[{messageType,text}]}`, RFC 7807, or Jetty HTML | `[{code, correlationId, messageType, text, timestamp}]` everywhere | 🔴 |

## 4. Registry API details

### 4.1 Create shell: same contract

Request, identical for both registries:

```http
POST /shell-descriptors
Edc-Bpn: default-tenant
Content-Type: application/json

{
  "id": "urn:uuid:c50e42478568", "idShort": "VehicleCombustion",
  "assetKind": "Instance", "assetType": "Vehicle",
  "globalAssetId": "urn:uuid:global-c50e42478568",
  "description": [{"language": "en", "text": "parity test twin"}],
  "specificAssetIds": [
    {"name": "manufacturerId", "value": "BPNL00000003AYRE",
     "externalSubjectId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": "PUBLIC_READABLE"}]}},
    {"name": "manufacturerPartId", "value": "MPI-c50e42478568", "externalSubjectId": {"…": "PUBLIC_READABLE"}},
    {"name": "digitalTwinType", "value": "PartInstance", "externalSubjectId": {"…": "PUBLIC_READABLE"}},
    {"name": "partInstanceId", "value": "PIN-c50e42478568",
     "externalSubjectId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": "BPNL00000003AYRE"}]}}
  ],
  "submodelDescriptors": [{
    "id": "urn:uuid:sm-SerialPart-c50e42478568", "idShort": "SerialPart",
    "semanticId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference", "value": "urn:samm:io.catenax.serial_part:3.0.0#SerialPart"}]},
    "endpoints": [{"interface": "SUBMODEL-3.0", "protocolInformation": {
      "href": "https://edc.provider.invalid/api/public/urn:uuid:sm-SerialPart-c50e42478568",
      "endpointProtocol": "HTTP", "endpointProtocolVersion": ["1.1"],
      "subprotocol": "DSP", "subprotocolBody": "id=asset-1;dspEndpoint=https://edc.provider.invalid/api/v1/dsp",
      "subprotocolBodyEncoding": "plain",
      "securityAttributes": [{"type": "NONE", "key": "NONE", "value": "NONE"}]}}]
  }]
}
```

Both registries returned `201` with the stored descriptor and a `createdAt`
timestamp. Tractus-X also adds empty `displayName: []` and `description: []`
arrays. BaSyx leaves out empty arrays and sorts the keys.

### 4.2 Duplicate create: 400 vs 409

```http
POST /shell-descriptors          (same body again)
```

Tractus-X: `400`

```json
{"messages": [{"messageType": "Error", "text": "An AssetAdministrationShell for the given identification does already exists."}]}
```

BaSyx: `409`

```json
[{"code": "409", "correlationId": "AASR-409-PostAssetAdministrationShellDescriptor-Conflict-Conflict-Exists",
  "messageType": "Error", "text": "409 Conflict: AAS with given id already exists", "timestamp": "2026-10-26T10:20:27Z"}]
```

### 4.3 Not found and other errors

```http
GET /shell-descriptors/dXJuOnV1aWQ6bm9wZQ        (urn:uuid:nope)
```

| Registry | Status | Body |
|---|---|---|
| Tractus-X | 404 | `{"messages":[{"messageType":"Error","text":"Shell for identifier urn:uuid:nope not found"}]}` |
| BaSyx | 404 | `[{"code":"404","correlationId":"AASR-404-GetAssetAdministrationShellDescriptorById-NotFound-NotFound","messageType":"Error","text":"404 Not Found: AAS Descriptor not found","timestamp":"…"}]` |

| Request | Tractus-X | BaSyx |
|---|---|---|
| `POST /shell-descriptors {"idShort":"x"}` | `400 {"messages":[{"code":"idShort",…},{"code":"id","text":"must not be null"}]}` | `400 [{"code":"400",…,"text":"required field 'id' is zero value."}]` |
| `POST … {"assetKind":"BAD"}` | `400` RFC 7807 `{"type","title","status","detail","instance"}` | `400 [{…}]` |
| `GET /shell-descriptors/%%%` | `400` Jetty HTML page | `400 [{…,"text":"… COMMON-APIPARAM-ALPHABET expected base64url"}]` |
| `GET /shell-descriptors?limit=0` | `400 {"messages":[…]}` | `400 [{…}]` |
| `GET /shell-descriptors?cursor=garbage` | `200`, page 1 | `400 [{…,"text":"… COMMON-APIPARAM-DECODE illegal base64 data"}]` |

### 4.4 Empty lookup result

```http
GET /lookup/shells?assetIds=<b64({"name":"manufacturerPartId","value":"does-not-exist"})>
```

| Registry | Body |
|---|---|
| Tractus-X | `{"paging_metadata": {}, "result": []}` |
| BaSyx | `{"paging_metadata": {}}` |

BaSyx documents this in its OpenAPI spec: *"For DTR compatibility,
empty-asset-link requests … may return {}"*.

## 5. `Edc-Bpn` visibility with the bundle defaults

In Catena-X, the EDC data plane sets `Edc-Bpn` to the BPN of the consumer
that negotiated the registry asset. The registry has to filter what each
consumer sees.

### 5.1 Read a shell as BPN B (public IDs only)

```http
GET /shell-descriptors/dXJuOnV1aWQ6YzUwZTQyNDc4NTY4
Edc-Bpn: BPNL00000003AZQP
```

Tractus-X: `200`. It returns only the public, wildcard-allowed IDs and hides
`idShort`, `globalAssetId`, `assetKind`, `assetType` and `description`:

```json
{"description": [], "displayName": [], "id": "urn:uuid:c50e42478568",
 "specificAssetIds": [
   {"name": "digitalTwinType", "value": "PartInstance", "externalSubjectId": {"…": "PUBLIC_READABLE"}},
   {"name": "manufacturerPartId", "value": "MPI-c50e42478568", "externalSubjectId": {"…": "PUBLIC_READABLE"}}],
 "submodelDescriptors": ["…"], "createdAt": "…"}
```

BaSyx with the bundle defaults: `200`. It returns **the full descriptor,
including BPN A's `partInstanceId`**:

```json
{"assetKind": "Instance", "assetType": "Vehicle", "globalAssetId": "urn:uuid:global-c50e42478568",
 "id": "urn:uuid:c50e42478568", "idShort": "VehicleCombustion", "description": ["…"],
 "specificAssetIds": [
   {"name": "manufacturerId", "value": "BPNL00000003AYRE", "…": "PUBLIC_READABLE"},
   {"name": "manufacturerPartId", "value": "MPI-c50e42478568", "…": "PUBLIC_READABLE"},
   {"name": "digitalTwinType", "value": "PartInstance", "…": "PUBLIC_READABLE"},
   {"name": "partInstanceId", "value": "PIN-c50e42478568", "externalSubjectId": {"keys": [{"value": "BPNL00000003AYRE"}]}}],
 "submodelDescriptors": ["…"]}
```

### 5.2 Discover a twin by a restricted ID

```http
GET /lookup/shells?assetIds=<b64({"name":"partInstanceId","value":"PIN-c50e42478568"})>
Edc-Bpn: BPNL00000003AZQP
```

| Registry | Response |
|---|---|
| Tractus-X | `{"paging_metadata": {}, "result": []}` |
| BaSyx (defaults) | `{"paging_metadata": {}, "result": ["urn:uuid:c50e42478568"]}` |

### 5.3 Why

In BaSyx Go, `Edc-Bpn` is never a filter on its own. `EdcBpnHeaderMiddleware`
copies the header into the request's claims, and only ABAC formulas read those
claims. With the bundle defaults, nothing filters the response:

- `abac.enabled` is `false`.
- `GENERAL_ENABLECUSTOMMIDDLEWAREHEADERINJECTION` is `false` (the chart
  default).

## 6. Configure ABAC for Tractus-X style visibility

This configuration was deployed on the test cluster. The checks were run
against it and compared with the Tractus-X DTR. It is based on the upstream
[`BaSyxDigitalTwinRegistryExample`](https://github.com/eclipse-basyx/basyx-go-components/tree/main/examples/BaSyxDigitalTwinRegistryExample),
which follows the Tractus-X DTR
[cross-cutting concept](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/blob/main/docs/architecture/6-crosscutting-concepts.md).
The upstream rules were changed in three ways to behave more like the
Tractus-X DTR:

- An owner rule
- The wildcard-type restriction
- Public IDs are shown even when the `Edc-Bpn` header is missing

### 6.1 Concept mapping

| Tractus-X DTR | BaSyx ABAC equivalent |
|---|---|
| `REGISTRY_IDM_OWNING_TENANT_ID` (owner sees everything) | Formula `owner_read`: role `view_digital_twin` **and** claim `Edc-Bpn` equals the owner BPN. Callers with role `add_digital_twin` (the provider's own apps) also see everything. |
| Roles `view`, `add`, `update` and `delete_digital_twin` | The same role names in the token claim `role`, used by `can_create`, `can_update`, `can_delete` and `consumer_read`. |
| `externalSubjectId` contains the caller's BPN → the ID is visible | `$eq` of `CLAIM Edc-Bpn` and `$aasdesc#specificAssetIds[].externalSubjectId.keys[].value` |
| `PUBLIC_READABLE` only for `manufacturerPartId` and `digitalTwinType` | A `$match` of the key value `PUBLIC_READABLE` **and** the `name` on the same element. This works for reads only (see 6.5). |
| Non-owners see a reduced shell (no `idShort`, `globalAssetId`, `assetKind`, `assetType`, `description`) | A `FILTERLIST` that keeps those fragments only when `bpn_match` is true |
| A shell is visible only if at least one of its IDs is visible | The route formula `consumer_read` is the same expression as `visible_id` |
| The EDC calls the DTR with `Edc-Bpn` (and a token when authentication is on) | `GENERAL_ENABLECUSTOMMIDDLEWAREHEADERINJECTION=true`. The EDC uses a technical client that has only `view_digital_twin`. |

### 6.2 Identity provider requirements

- An OIDC issuer that the DTR pod can reach. The `iss` in every token must be
  exactly the issuer in the trust list. In the test, Keycloak ran with
  `KC_HOSTNAME=http://keycloak.basyx.svc.cluster.local:8080`, so tokens fetched
  through a port-forward still had the in-cluster issuer.
- A multi-valued claim `role`. In the test, Keycloak's user-attribute mapper
  `role` filled it.
- An audience that matches the trust list: `discovery-service` in the test.
- Two kinds of identity:
  - Provider apps that upload data, with all four roles. In the test this was
    the user `provider`.
  - The EDC data plane technical client, with `view_digital_twin` only. In the
    test this was the user `edc-dtr-reader`.

  Use client-credentials clients in production.

`hack/dtr-poc/local_stack.py --abac` creates a minimal test realm with exactly
these two users. Their passwords are generated at install time and stored only
in the Secret `keycloak-test-users`.

### 6.3 Helm values

These values go under `tx-data-provider`, on top of the BaSyx profile:

```yaml
digital-twin-basyx-bundle:
  basyx:
    digitalTwinRegistry:
      general:
        # Turn the Edc-Bpn request header into an ABAC claim. Chart default: false.
        enableCustomMiddlewareHeaderInjection: true
      abac:
        enabled: true
        trustList: |
          [
            {
              "issuer": "http://keycloak.basyx.svc.cluster.local:8080/realms/basyx",
              "audience": "discovery-service",
              "scopes": ["email", "profile"]
            }
          ]
        accessRules: |
          <the JSON from 6.4, hack/dtr-poc/access-rules-tractusx.json>
```

The chart then mounts the rules and the trust list at `/security_env` and sets
these variables:

- `ABAC_ENABLED=true`
- `ABAC_MODELPATH=/security_env/access-rules.json`
- `OIDC_TRUSTLISTPATH=/security_env/trustlist.json`

The explicit environment variables override `ABAC_ENABLED: false` from the
bundle's `environment.common`. The DTR log shows
`OIDC verifier initialized issuer=…/realms/basyx audience=discovery-service`.

### 6.4 Access rules

The tested file is
[`hack/dtr-poc/access-rules-tractusx.json`](../../../../hack/dtr-poc/access-rules-tractusx.json).
Replace `default-tenant` in `owner_read` with your provider BPN. That is the
value the Tractus-X DTR has in `REGISTRY_IDM_OWNING_TENANT_ID`.

```json
{
  "AllAccessPermissionRules": {
    "DEFATTRIBUTES": [
      { "name": "anonym_attr", "attributes": [ { "GLOBAL": "ANONYMOUS" } ] },
      { "name": "role_attr", "attributes": [ { "CLAIMPATH": "/role" } ] }
    ],
    "DEFOBJECTS": [
      { "name": "description", "objects": [ { "ROUTE": "/description" } ] },
      { "name": "assetlinks", "objects": [ { "ROUTE": "/lookup/shells" }, { "ROUTE": "/lookup/shellsByAssetLink" } ] },
      { "name": "shells", "objects": [ { "ROUTE": "/lookup/shells/*" } ] },
      { "name": "all_shell_descriptors", "objects": [ { "DESCRIPTOR": "$aasdesc(\"*\")" } ] }
    ],
    "DEFACLS": [
      { "name": "anonymous_read", "acl": { "USEATTRIBUTES": "anonym_attr", "RIGHTS": ["READ"], "ACCESS": "ALLOW" } },
      { "name": "token_read",   "acl": { "USEATTRIBUTES": "role_attr", "RIGHTS": ["READ"],   "ACCESS": "ALLOW" } },
      { "name": "token_create", "acl": { "USEATTRIBUTES": "role_attr", "RIGHTS": ["CREATE"], "ACCESS": "ALLOW" } },
      { "name": "token_update", "acl": { "USEATTRIBUTES": "role_attr", "RIGHTS": ["UPDATE"], "ACCESS": "ALLOW" } },
      { "name": "token_delete", "acl": { "USEATTRIBUTES": "role_attr", "RIGHTS": ["DELETE"], "ACCESS": "ALLOW" } }
    ],
    "DEFFORMULAS": [
      { "name": "always_true", "formula": { "$boolean": true } },
      { "name": "can_create", "formula": { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "add_digital_twin" } ] } },
      { "name": "can_update", "formula": { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "update_digital_twin" } ] } },
      { "name": "can_delete", "formula": { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "delete_digital_twin" } ] } },
      { "name": "owner_read", "formula": { "$or": [
          { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "add_digital_twin" } ] },
          { "$and": [
            { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "view_digital_twin" } ] },
            { "$eq": [ { "$attribute": { "CLAIM": "Edc-Bpn" } }, { "$strVal": "default-tenant" } ] }
          ] }
      ] } },
      { "name": "consumer_read", "formula": { "$and": [
          { "$contains": [ { "$attribute": { "CLAIMPATH": "/role" } }, { "$strVal": "view_digital_twin" } ] },
          { "$or": [
            { "$eq": [ { "$attribute": { "CLAIM": "Edc-Bpn" } }, { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" } ] },
            { "$match": [
              { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" }, { "$strVal": "PUBLIC_READABLE" } ] },
              { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].name" }, { "$strVal": "manufacturerPartId" } ] }
            ] },
            { "$match": [
              { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" }, { "$strVal": "PUBLIC_READABLE" } ] },
              { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].name" }, { "$strVal": "digitalTwinType" } ] }
            ] }
          ] }
      ] } },
      { "name": "visible_id", "formula": { "$or": [
          { "$eq": [ { "$attribute": { "CLAIM": "Edc-Bpn" } }, { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" } ] },
          { "$match": [
            { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" }, { "$strVal": "PUBLIC_READABLE" } ] },
            { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].name" }, { "$strVal": "manufacturerPartId" } ] }
          ] },
          { "$match": [
            { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" }, { "$strVal": "PUBLIC_READABLE" } ] },
            { "$eq": [ { "$field": "$aasdesc#specificAssetIds[].name" }, { "$strVal": "digitalTwinType" } ] }
          ] }
      ] } },
      { "name": "bpn_or_public_key", "formula": { "$or": [
          { "$eq": [ { "$attribute": { "CLAIM": "Edc-Bpn" } }, { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" } ] },
          { "$eq": [ { "$strVal": "PUBLIC_READABLE" }, { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" } ] }
      ] } },
      { "name": "bpn_match", "formula":
          { "$eq": [ { "$attribute": { "CLAIM": "Edc-Bpn" } }, { "$field": "$aasdesc#specificAssetIds[].externalSubjectId.keys[].value" } ] } }
    ],
    "rules": [
      { "USEACL": "anonymous_read", "USEOBJECTS": ["description"], "USEFORMULA": "always_true" },
      { "USEACL": "token_create", "USEOBJECTS": ["all_shell_descriptors", "assetlinks", "shells"], "USEFORMULA": "can_create" },
      { "USEACL": "token_update", "USEOBJECTS": ["all_shell_descriptors", "assetlinks", "shells"], "USEFORMULA": "can_update" },
      { "USEACL": "token_delete", "USEOBJECTS": ["all_shell_descriptors", "assetlinks", "shells"], "USEFORMULA": "can_delete" },
      { "USEACL": "token_read", "USEOBJECTS": ["all_shell_descriptors", "assetlinks", "shells"], "USEFORMULA": "owner_read" },
      { "USEACL": "token_read", "USEOBJECTS": ["all_shell_descriptors"], "USEFORMULA": "consumer_read",
        "FILTERLIST": [
          { "FRAGMENT": "$aasdesc#administration", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#displayName", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#description", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#assetKind", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#assetType", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#globalAssetId", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#idShort", "USEFORMULA": "bpn_match" },
          { "FRAGMENT": "$aasdesc#specificAssetIds[]", "USEFORMULA": "visible_id", "MATCH": true },
          { "FRAGMENT": "$aasdesc#specificAssetIds[].externalSubjectId.keys[]", "USEFORMULA": "bpn_or_public_key", "MATCH": true }
        ] },
      { "USEACL": "token_read", "USEOBJECTS": ["assetlinks"], "USEFORMULA": "consumer_read" }
    ]
  }
}
```

What each rule does:

1. **`description`**: anyone can read `/description`.
2. **Write rules**: create, update and delete need the matching role. The
   `Edc-Bpn` header never grants write access.
3. **`owner_read`**: provider apps (`add_digital_twin`), or a reader whose
   `Edc-Bpn` is the owner BPN, get the full descriptor without filters.
4. **`consumer_read` on descriptors**: a reader sees a shell only if at least
   one of its IDs is visible. Only the visible `specificAssetIds` and only the
   visible `externalSubjectId` keys are returned. The descriptive fields are
   returned only when the caller's BPN matches one of the IDs.
5. **`consumer_read` on lookups**: discovery needs a token with
   `view_digital_twin`. BaSyx then also applies its built-in per-link check
   (6.5).
6. **`/lookup/shells/{id}`**: only the owner and writers can call it. Other
   callers get `403`; see 6.5.

The bulk and query routes are not listed, so they return `403`. If you need
them, add `{ "ROUTE": "/bulk/*" }` and `{ "ROUTE": "/query/*" }` objects.

### 6.5 Results with ABAC on

Writes used the provider token. Reads used the EDC-reader token plus the
`Edc-Bpn` shown. The Tractus-X DTR received the same calls without a token,
because its authentication was off.

| Check | Tractus-X | BaSyx + ABAC | Result |
|---|---|---|---|
| Create as provider | `201` | `201` | ✅ |
| Create without token, or as EDC reader | n/a (authentication off) | `403` | as Tractus-X with authentication on |
| Read without token | n/a | `403` | as Tractus-X with authentication on |
| Read as provider (no `Edc-Bpn`) | all 4 IDs, all fields (owner header) | all 4 IDs, all fields | ✅ |
| Read as owner (`Edc-Bpn: default-tenant`) | all 4 IDs, all fields | all 4 IDs, all fields | ✅ |
| Read as BPN A | `manufacturerPartId`, `digitalTwinType`, `partInstanceId`, all descriptive fields | the same | ✅ |
| Read as BPN B | `manufacturerPartId`, `digitalTwinType`; no `idShort`, `globalAssetId`, `assetKind`, `assetType` or `description` | the same | ✅ |
| Read with no `Edc-Bpn` | `manufacturerPartId`, `digitalTwinType`; reduced fields | the same | ✅ |
| List as BPN B | 1 shell | 1 shell | ✅ |
| Lookup `manufacturerPartId` as BPN B, or with no header | found | found | ✅ |
| Lookup `partInstanceId` as BPN A | found | found | ✅ |
| Lookup `partInstanceId` as BPN B (GET and `shellsByAssetLink`) | empty | empty | ✅ |
| Lookup `globalAssetId` as BPN B | found | found | ✅ |
| Lookup a `PUBLIC_READABLE` `manufacturerId` as BPN B | empty | **found** | 🔴 built in |
| `GET /lookup/shells/{id}` as owner | 4 links | 5 links (+ `globalAssetId`) | 🟡 built in |
| `GET /lookup/shells/{id}` as BPN B | 2 public links | `403` | 🔴 by design of the rules |
| Submodel descriptors as BPN B | 1 | 1 | ✅ |
| Delete as EDC reader | n/a | `403` | as Tractus-X with authentication on |
| Delete as provider | `204` | `204` | ✅ |

Here is a captured BaSyx response for BPN B. It matches the Tractus-X
response in Section 5.1, apart from field order and `createdAt`:

```http
GET /digital-twin-registry/shell-descriptors/dXJuOnV1aWQ6ZTMzZjNiMDZhY2Fh
Authorization: Bearer <edc-dtr-reader token>
Edc-Bpn: BPNL00000003AZQP
```

```json
{"createdAt": "2026-10-26T10:35:29.811233Z", "id": "urn:uuid:e33f3b06aca0",
 "specificAssetIds": [
   {"externalSubjectId": {"keys": [{"type": "GlobalReference", "value": "PUBLIC_READABLE"}], "type": "ExternalReference"},
    "name": "manufacturerPartId", "value": "MPI-e33f3b06aca0"},
   {"externalSubjectId": {"keys": [{"type": "GlobalReference", "value": "PUBLIC_READABLE"}], "type": "ExternalReference"},
    "name": "digitalTwinType", "value": "PartInstance"}],
 "submodelDescriptors": ["…"]}
```

A call without a token returns:

```json
[{"code": "403", "correlationId": "Middleware-403-Rules-Forbidden-Denied", "messageType": "Error", "text": "access denied", "timestamp": "2026-10-26T10:35:29Z"}]
```

These differences remain, and the rules cannot remove them:

1. **Lookup ignores the wildcard-type list.** BaSyx builds the per-link
   discovery check in code (`buildAssetLinkQueryForRoot` in
   `internal/digitaltwinregistry/custom_discovery_service.go`). The rule is
   "exact link match AND (`Edc-Bpn` == key OR key == `PUBLIC_READABLE`)", for
   any `name`.
   **Mitigation:** put `PUBLIC_READABLE` only on `manufacturerPartId` and
   `digitalTwinType`. Tractus-X does not expose other public types to
   non-owners anyway. With that data rule the results are the same.
2. **`GET /lookup/shells/{id}` cannot be filtered.** The route is either
   allowed or denied. These rules deny it to consumers. Tractus-X instead
   returns the visible links. Catena-X consumers discover twins with
   `/lookup/shells` and `/shellsByAssetLink`, not with this route.
3. **`globalAssetId` is always a public discovery key** and appears in the
   asset links. Tractus-X also found the twin by `globalAssetId` for BPN B, so
   lookups behave the same.

### 6.6 Security notes

- With header injection on, the DTR trusts the `Edc-Bpn` header. Only the
  EDC data plane may reach the DTR. Use a `NetworkPolicy`, no public ingress,
  and strip `Edc-Bpn` at any gateway. This is the same trust model as the
  Tractus-X DTR.
- A stronger setup, as recommended upstream: put the BPN into the token claim
  `Edc-Bpn` at the identity provider, and set
  `enableCustomMiddlewareHeaderInjection: false`.
- `owner_read` hard-codes the owner BPN. Use one rule file per tenant, which
  fits the one-instance-per-tenant design of the bundle.

## 7. Submodel data service: `simple-data-backend` vs BaSyx Submodel Repository

### 7.1 API comparison

| Operation | Verdict | `simple-data-backend` | BaSyx Submodel Repository | What changes |
|---|---|---|---|---|
| Store data | 🔴 | `POST /{id}` with any JSON → `200`, empty body | `POST /submodel-repo/submodels` with an AAS `Submodel` → `201` + submodel. Raw SAMM JSON → `400 "Unexpected property: childItems"`. | Wrap every payload in an AAS submodel (7.3). |
| Read value (`$value`) | 🔴 | `GET /{id}/$value` → the stored JSON, unchanged | `GET /submodel-repo/submodels/{b64(id)}/$value` → value-only JSON, **numbers and booleans as strings** | IDs in URLs are Base64URL. The types change (7.4). |
| Read without `$value` | 🔴 | `GET /{id}` → the same JSON | `GET …/submodels/{b64}` → the full AAS structure | Different payload |
| Delete | 🟡 | `DELETE /{id}` | `DELETE …/submodels/{b64}` | Encoded ID |
| Not found | 🟡 | `404` Spring `{"timestamp","status":404,"error":"Not Found","path"}` | `404 [{"code":"404","correlationId":"SMREPO-404-GetSubmodelByIDValueOnly-…"}]` | Error parsing |
| Health | ➕ | – | `GET /submodel-repo/health` → `200` | – |
| Element-level access | ➕ | – | `…/submodel-elements/{idShortPath}`, `$metadata`, `$reference`, `$path` | – |
| Persistence | 🔴 | In memory, lost on restart | PostgreSQL, shared schema with the DTR | Back up the data |
| Validation | 🔴 | None | Full AAS metamodel | Invalid payloads are rejected |

The context path is `/submodel-repo` (`paths.submodelRepository` in the BaSyx
chart), not `/submodel-repository`.

### 7.2 The current upload format is rejected

`charts/tx-data-provider/resources/transform-and-upload.py` posts the raw SAMM
payload:

```http
POST /submodel-repo/submodels
Content-Type: application/json

{"catenaXId": "urn:uuid:0733946c-…", "childItems": [ … ]}
```

```json
400 [{"code": "400", "correlationId": "SMREPO-400-DefaultErrorHandler-BadRequest-ParseRequest",
      "messageType": "Error", "text": ": Unexpected property: childItems"}]
```

### 7.3 Round trip with an AAS wrapper

Each SAMM payload was converted to an AAS `Submodel` as follows:

- An object becomes a `SubmodelElementCollection`.
- An array becomes a `SubmodelElementList`, with no `idShort` on its children.
- A scalar becomes a `Property`. Strings and dates use `xs:string`, integers
  use `xs:long`, floats use `xs:double` and booleans use `xs:boolean`.

Input to `simple-data-backend` (and the source for the AAS wrapper):

```json
{"catenaXId": "urn:uuid:0733946c-59c6-41ae-9570-cb43a6e4c79e",
 "childItems": [{
   "validityPeriod": {"validFrom": "2023-03-21T08:17:29.187+01:00", "validTo": "2024-07-01T16:10:00.000+01:00"},
   "catenaXId": "urn:uuid:aad27ddb-43aa-4e42-98c2-01e529ef127c",
   "quantity": {"unit": "unit:piece", "value": 1},
   "businessPartner": "BPNL00000003AYRE",
   "createdOn": "2022-02-03T14:48:54.709Z", "lastModifiedOn": "2022-02-03T14:48:54.709Z"}]}
```

Request to BaSyx (shortened):

```http
POST /submodel-repo/submodels
Content-Type: application/json

{"modelType": "Submodel", "id": "urn:uuid:e1b8ba17-9cce-4a13-ba6e-7185a5adfae5", "kind": "Instance",
 "idShort": "SingleLevelBomAsPlanned",
 "semanticId": {"type": "ExternalReference", "keys": [{"type": "GlobalReference",
   "value": "urn:samm:io.catenax.single_level_bom_as_planned:3.0.0#SingleLevelBomAsPlanned"}]},
 "submodelElements": [
   {"idShort": "catenaXId", "modelType": "Property", "valueType": "xs:string", "value": "urn:uuid:0733946c-…"},
   {"idShort": "childItems", "modelType": "SubmodelElementList", "typeValueListElement": "SubmodelElementCollection",
    "value": [{"modelType": "SubmodelElementCollection", "value": [
      {"idShort": "quantity", "modelType": "SubmodelElementCollection", "value": [
        {"idShort": "unit",  "modelType": "Property", "valueType": "xs:string", "value": "unit:piece"},
        {"idShort": "value", "modelType": "Property", "valueType": "xs:long",   "value": "1"}]},
      "…"]}]}]}
```

`201`.

Read the data back:

```http
GET /submodel-repo/submodels/dXJuOnV1aWQ6ZTFiOGJhMTctOWNjZS00YTEzLWJhNmUtNzE4NWE1YWRmYWU1/$value
```

| `simple-data-backend` `GET /{id}/$value` | BaSyx `GET …/{b64}/$value` |
|---|---|
| `"quantity": {"unit": "unit:piece", "value": 1}` | `"quantity": {"unit": "unit:piece", "value": "1"}` |

### 7.4 `$value` returns every scalar as a string

A probe that posted one `Property` of each `valueType` and read its `$value`
returned:

```json
{"pboolean": "true", "pdate": "2022-02-03", "pdateTime": "2022-02-03T14:48:54.709+00:00",
 "pdecimal": "12", "pdouble": "12", "pfloat": "12", "pint": "12", "pinteger": "12",
 "plong": "12", "pshort": "12", "pstring": "abc"}
```

- Numbers and booleans come back as JSON strings for every numeric type.
- With `xs:dateTime`, `Z` is rewritten to `+00:00`. Storing timestamps as
  `xs:string` keeps them byte-identical.

Across all 112 aspect payloads in `Testdata_AsBuilt-combustion.json`:

| Aspect | Payloads | Exact after round trip |
|---|---|---|
| PartAsPlanned | 24 | 24 |
| PartSiteInformationAsPlanned | 22 | 22 |
| SingleLevelBomAsPlanned | 24 | 10 |
| SingleLevelUsageAsPlanned | 20 | 0 |
| SecondaryMaterialContentCalculated | 22 | 0 |
| **Total** | **112** | **56** (simple-data-backend: 112) |

There were 424 changed leaf values: 240 integers, 30 floats and 154 booleans
came back as strings. All payload structures and strings were kept. Consumers
that validate against the SAMM JSON schema would reject `"value": "1"` where
the schema requires a number.

### 7.5 Data path through the EDC

With `simple-data-backend`, the path is:

1. The EDC asset has `baseUrl = http://<release>-simple-data-backend:8080` and
   `proxyPath = true`.
2. The descriptor `href` is `<dataplane>/api/public/<submodelId>`.
3. The consumer calls `href + /$value`, and the backend receives
   `GET /<submodelId>/$value`.

With BaSyx, the same pattern works if the IDs are encoded:

1. The EDC asset has
   `baseUrl = http://<fullname>-submodel-repository:8080/submodel-repo/submodels`.
2. The descriptor `href` is `<dataplane>/api/public/<base64url(submodelId)>`.
3. The consumer calls `href + /$value`, and BaSyx receives
   `GET /submodel-repo/submodels/<b64>/$value`.

This part was checked by reasoning only. **EDC negotiation and data plane
transfer were not run in this test.**

## 8. What changes if you migrate

### Registry (Tractus-X DTR → BaSyx DTR)

| Topic | Change required |
|---|---|
| Base URL | `…/api/v3` becomes `…/digital-twin-registry`. Update `registryUrl` and the EDC `data.core.digitalTwinRegistry` asset `baseUrl`. The resource paths below the base are the same. |
| Visibility | **Required.** Apply [Section 6](#6-configure-abac-for-tractus-x-style-visibility): ABAC + OIDC + header injection + Tractus-X style rules. Without it, every partner who can reach the DTR asset sees every restricted ID. |
| EDC DTR asset | Add OAuth2 data-address properties so the data plane gets a `view_digital_twin` token. Keep `Edc-Bpn` forwarding. |
| `PUBLIC_READABLE` data | Put `PUBLIC_READABLE` only on `manufacturerPartId` and `digitalTwinType`. BaSyx lookups treat any public type as discoverable. |
| Owner identity | Replace `REGISTRY_IDM_OWNING_TENANT_ID` with the owner BPN in `owner_read`. Provider apps need a token with `add_digital_twin`. |
| `/description` | Consumers that check IDTA 3.0 or 3.1 registry or discovery profiles will not find one. |
| Error handling | Accept a top-level array `[{code, correlationId, messageType, text, timestamp}]` as well as `messages[]`. |
| Status codes | Duplicate create returns `409` instead of `400`. `PUT` on a missing ID creates it (`201`). `GET` asset links after deleting them returns `404`. |
| Empty lookup | Read `result` with a default (`body.get("result", [])`). |
| Paging | Do not depend on getting a cursor on the last page. Invalid cursors return `400`. |
| Asset links | Expect `globalAssetId` in the asset links. `POST /lookup/shells/{id}` appends links and does not deduplicate them. |
| Granular access control | `POST /submodel-descriptor/authorized` does not exist. Tractus-X `REGISTRY_USE_GRANULAR_ACCESS_CONTROL=true` setups need a redesign. |
| Data migration | There is no automatic tool and switching engines is not a Helm rollback. Export all descriptors from Tractus-X as the owner, page by page, and re-POST them to BaSyx with a provider token. Then compare the counts and run spot lookups for each BPN. |
| Images | Pin the multi-arch index digests so arm64 and amd64 nodes can run them. |

### Data service (`simple-data-backend` → BaSyx Submodel Repository)

| Topic | Change required |
|---|---|
| Upload | Change `transform-and-upload.py` to wrap every payload in an AAS `Submodel` (Section 7.3) and post it to `/submodel-repo/submodels`. |
| IDs in URLs | Base64URL-encode the submodel ID in the descriptor `href` and in any direct calls. |
| EDC asset | Set `baseUrl` to `…/submodel-repo/submodels` and keep `proxyPath: true`. |
| Typed values | **Blocker for SAMM consumers.** `$value` returns strings for numbers and booleans. Report this upstream or check a newer BaSyx release. |
| Timestamps | Store them as `xs:string`. `xs:dateTime` changes `Z` to `+00:00`. |
| Configuration | Set `GENERAL_SUBMODELREGISTRYINTEGRATION: false` unless a Submodel Registry is deployed. Set `GENERAL_EXTERNALURL` to the real external URL. |
| Persistence | Data now survives pod restarts because it is stored in PostgreSQL. Include the repository data in backups. |
| Security | The repository uses the same ABAC model as the DTR (`submodelRepository.abac`). Turn it on if the repository can be reached in any way other than through the EDC. |

## 9. Not covered

- A full umbrella end-to-end test: EDC catalog, negotiation, OAuth2 data
  addresses and data plane transfer to either backend, and IRS or consumer
  apps.
- Tractus-X DTR with authentication turned on. Its visibility was compared
  with authentication off.
- ABAC on the Submodel Repository.
- Tractus-X granular access control mode.
- Bulk and query endpoints with ABAC rules
- Performance, high availability and cross-version schema rollback.

## 10. Reproduce

The scripts in `hack/dtr-poc/` install both stacks and send every request in
this report. They pass `--context` or `--kube-context` to every command and
never use your current kube context. Generated test passwords go to kubectl
through stdin only.

1. Resolve the chart dependencies:

   ```bash
   python -m pip install -r hack/dtr-poc/requirements.txt
   python hack/dtr-poc/dependencies.py
   ```

2. Create a separate cluster without changing your current kube context:

   ```bash
   minikube start -p basyx-dtr-test --cpus=4 --memory=6g --kubernetes-version=v1.30.0 --keep-context
   ```

3. Install the Tractus-X stack (namespace `txdtr`) and the BaSyx stack
   (namespace `basyx`, with its external PostgreSQL and the Submodel
   Repository), using the values from [Section 1](#1-test-setup):

   ```bash
   python hack/dtr-poc/local_stack.py --context basyx-dtr-test
   ```

4. Run the registry and submodel comparisons (Sections 3, 4, 5 and 7):

   ```bash
   python hack/dtr-poc/parity.py registry --context basyx-dtr-test --out .dtr-poc-artifacts/parity
   python hack/dtr-poc/parity.py submodel --context basyx-dtr-test --out .dtr-poc-artifacts/parity
   ```

5. Deploy Keycloak, turn on the ABAC values from Section 6.3 and run the
   visibility comparison (Section 6). The existing database is kept.

   ```bash
   python hack/dtr-poc/local_stack.py --context basyx-dtr-test --only basyx --abac
   python hack/dtr-poc/parity.py visibility --context basyx-dtr-test --out .dtr-poc-artifacts/parity
   ```

   Each suite prints one line per call and writes the full requests and
   responses to `<suite>-parity.json` (`submodel-parity.json` for the submodel
   suite). The `same projection` count is strict: an empty lookup counts as
   different because BaSyx leaves out the `result` key. That is why the
   visibility suite reports 14 where Section 6.5 counts 16 matching results.

6. Remove the cluster when you are done:

   ```bash
   minikube delete -p basyx-dtr-test
   ```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
