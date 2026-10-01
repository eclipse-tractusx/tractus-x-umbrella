<!-- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Evaluate an optional BaSyx DTR

The `tx-data-provider` chart can select BaSyx DTR instead of its default
Tractus-X DTR. Each evaluated enterprise has its own DTR instance, PostgreSQL
instance/database/role/schema, Secret and persistent storage. This is an
isolated deployment profile, not an automatic replacement or migration.

## Run the self-contained test

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

## Install an instance for your application

Generate tenant values and separately prepare a new PostgreSQL instance,
least-privilege database role, owned schema, persistent storage and database
Secret before installing the Helm chart. Follow the
[bundle installation guide](../../../../charts/digital-twin-basyx-bundle/README.md).

BaSyx uses `/digital-twin-registry` as its API base. Applications register
descriptors and Submodel endpoint metadata there; actual Submodel data still
comes from the application's data service. No supplier app, consumer app,
EDC data exchange, public ingress or authentication setup is included.

Keep the external database and storage when uninstalling the DTR application.
Reinstalling the same pinned version restores access to its retained data.
Switching Registry engines or downgrading a schema requires a separate plan.
