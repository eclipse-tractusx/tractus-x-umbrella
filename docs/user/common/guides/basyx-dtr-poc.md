<!-- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Evaluate an optional BaSyx DTR

The `tx-data-provider` chart can select the [Eclipse BaSyx](https://github.com/eclipse-basyx/charts)
Digital Twin Registry (DTR) instead of its default Tractus-X DTR. There are two ways to use it:

- [In the umbrella data-exchange scenario](#run-basyx-in-the-umbrella-data-exchange-scenario):
  the data provider uses the BaSyx DTR behind its EDC, exactly like the `digital-twin-bundle`.
  This is the quickest way to try it.
- [As an isolated tenant profile](#run-the-self-contained-test) with an externally
  provisioned PostgreSQL per tenant. This is not an automatic replacement or migration.

## Run BaSyx in the umbrella data-exchange scenario

The overlay [`values-adopter-data-exchange-basyx.yaml`](../../../../charts/umbrella/values-adopter-data-exchange-basyx.yaml)
is used together with `values-adopter-data-exchange.yaml`. It keeps the EDCs, the wallet stub,
the submodel server and the test data. Only the data provider's DTR is replaced:

| | Tractus-X DTR (`digital-twin-bundle`) | BaSyx DTR (`digital-twin-basyx-bundle`) |
|---|---|---|
| In-cluster API base | `http://umbrella-dataprovider-dtr:8080/api/v3` | `http://dataprovider-basyx-digital-twin-registry:8080/digital-twin-registry` |
| Ingress | `http://dataprovider-dtr.tx.test/semantics/registry/api/v3` | `http://dataprovider-basyx-dtr.tx.test/digital-twin-registry` |
| Database | bundled PostgreSQL 15 (`dataprovider-digital-twin-db`) | bundled PostgreSQL 16 (`dataprovider-basyx-db`); BaSyx requires 16+ |
| Schema | created by the DTR on startup | created by the BaSyx Configuration Service Job |

### Prerequisites

Follow your OS guide to start Minikube with the `ingress` and `ingress-dns` addons, and add
`dataprovider-basyx-dtr.tx.test` to your host resolution like the other `*.tx.test` hosts.
You also need `python3` on the machine running Helm.

### Install

```bash
./hack/helm-dependencies.bash
helm install umbrella charts/umbrella --namespace umbrella --create-namespace \
  -f charts/umbrella/values-adopter-data-exchange.yaml \
  -f charts/umbrella/values-adopter-data-exchange-basyx.yaml \
  --post-renderer python3 --post-renderer-args hack/dtr-poc/post-render.py
```

BaSyx chart 3.15.0 always renders a cert-manager `Issuer` (`internal-issuer`), even with TLS disabled.
The [post-renderer](../../../../hack/dtr-poc/post-render.py) removes only that object and needs no
Python packages. If cert-manager is installed in your cluster, you can omit the post-renderer.
Use the same flags for `helm upgrade`.

What happens during the install:

1. PostgreSQL `dataprovider-basyx-db` starts. The bundle renders the database Secret
   `dataprovider-basyx-database` for it.
2. The Job `dataprovider-basyx-configuration` waits for the database and creates the BaSyx schema.
   Until then the DTR Pod restarts with `relation "basyxsystem" does not exist`. This is expected.
3. With `tx-data-provider.seedTestdata: true` (the default in this overlay), the post-install Job
   `umbrella-dataprovider-post-install-testdata` registers the test shell descriptors in the
   BaSyx DTR. It also creates the EDC assets, policies and contract definitions for the
   submodels and for the DTR (`registry-asset`).

### Seeding on or off

Seeding is controlled by one switch:

```yaml
tx-data-provider:
  seedTestdata: true   # false: start with an empty BaSyx DTR and EDC
```

With `false`, run the Bruno folder `02-Provide_Data_Manually` to create the configuration yourself.

### Test with Bruno

Open the collection [`docs/common/api/bruno/Data-exchange-basyx`](../../../common/api/bruno/Data-exchange-basyx)
in [Bruno](https://www.usebruno.com/) and run the folders in order:

1. `01-Check_Seeded_Provider`: calls the BaSyx DTR directly (health, list, get, asset link lookup)
   and checks the seeded DTR asset in the provider EDC.
2. `02-Provide_Data_Manually`: only when `seedTestdata: false`. Creates the submodel data, the
   submodel and DTR EDC assets, the policies, the contract definition and the shell descriptor.
3. `03-Consume_Data_Via_EDC`: as the consumer (Alice). Negotiates access to the DTR asset,
   discovers a twin through the EDC data plane, reads the DSP subprotocol of its submodel
   descriptor, negotiates the submodel asset and fetches the data. If an EDR query returns an
   empty list, the negotiation is still running; wait a few seconds and send it again.

### Configure your own assets

The steps in `02-Provide_Data_Manually` are the reference. The parts that matter for BaSyx are:

- **DTR EDC asset**: set `dataAddress.baseUrl` to the in-cluster BaSyx API base,
  `http://dataprovider-basyx-digital-twin-registry:8080/digital-twin-registry`, without `/api/v3`.
  Set `proxyPath`, `proxyMethod`, `proxyQueryParams` and `proxyBody` to `"true"`. Set the
  `dct:type` `https://w3id.org/catenax/taxonomy#DigitalTwinRegistry` so consumers can find it.
- **Shell descriptor**: `POST {DTR}/shell-descriptors`. Each submodel endpoint carries
  `subprotocol: DSP`, `subprotocolBody: id=<submodel EDC asset id>;dspEndpoint=<provider DSP URL>`,
  and an `href` that points to the provider data plane (`.../api/public/<submodel id>`).
- **Identifiers in paths** are Base64URL encoded, for example `GET {DTR}/shell-descriptors/<base64url(id)>`.
  The same applies to `GET {DTR}/lookup/shells?assetIds=<base64url({"name":...,"value":...})>`.
- **Submodel EDC asset**: unchanged from the Tractus-X DTR scenario (`baseUrl` = submodel server).

### Differences to keep in mind

> [!WARNING]
> In this profile BaSyx runs with ABAC disabled. It does **not** apply Catena-X `externalSubjectId`
> (BPN) visibility: every caller that can reach the DTR sees all `specificAssetIds`, and lookups
> match regardless of the `Edc-Bpn` header. The Tractus-X DTR hides them from other BPNs. Use the
> EDC access policy (as in the Bruno collection) to restrict who can reach the DTR. Don't rely on
> `externalSubjectId` for confidentiality.

- Error response bodies differ between the two DTR implementations.
- The BaSyx images are pinned by digest for `amd64`.
- Persistence is enabled for the bundled PostgreSQL. `helm uninstall` keeps the PVC; delete it
  to start from scratch.

## Isolated tenant profile

The rest of this guide describes the isolated tenant profile. Each evaluated enterprise has its
own DTR instance, PostgreSQL instance/database/role/schema, Secret and persistent storage.

### Run the self-contained test

Check out the contribution branch and prepare Docker, Kind 0.23.0,
kubectl 1.30.0, Helm 3.21.3 and Python 3.12. From the repository root, install
the test requirements, resolve dependencies and run acceptance:

```bash
python -m pip install -r hack/dtr-poc/requirements.txt
python hack/dtr-poc/dependencies.py
python hack/dtr-poc/acceptance.py --artifacts .dtr-poc-artifacts/run-1
```

Use a new result directory for each run. The harness creates and removes its
own uniquely named Kind cluster. It requires no server credentials, business
application, existing Kubernetes context or production database.

The test installs two independent tenants and verifies initialization order,
descriptor CRUD, Asset Link, database credential isolation, persisted data
after Pod replacement, same-version Helm rollback and retained-database
reinstallation. It also compares default Tractus-X manifests to a pinned
upstream baseline. This last check is configuration regression, not a new
full Tractus-X Runtime installation.

See [test prerequisites, commands and results](../../../../hack/dtr-poc/README.md)
for the complete procedure.

### Install an instance for your application

Generate tenant values and separately prepare a new PostgreSQL instance,
least-privilege database role, owned schema, persistent storage and database
Secret before installing the Helm chart. Follow the
[bundle installation guide](../../../../charts/digital-twin-basyx-bundle/README.md).

BaSyx uses `/digital-twin-registry` as its API base. Applications register
descriptors and Submodel endpoint metadata there; actual Submodel data still
comes from the application's data service. This tenant profile includes no supplier app,
consumer app, EDC data exchange, public ingress or authentication setup; for EDC data
exchange use the [umbrella scenario](#run-basyx-in-the-umbrella-data-exchange-scenario).

Keep the external database and storage when uninstalling the DTR application.
Reinstalling the same pinned version restores access to its retained data.
Switching Registry engines or downgrading a schema requires a separate plan.
