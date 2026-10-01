<!-- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# BaSyx tenant deployment and acceptance

The intended replacement uses one BaSyx DTR instance and an independent
PostgreSQL instance, database, role, schema, Secret and PVC per enterprise.
The existing Tractus-X provider remains the default while the replacement is
validated. This directory prepares tenant values and runs disposable acceptance;
it does not provision or modify an existing enterprise.

## Quick start: disposable acceptance

Check out the contribution branch and have Docker running. Put Kind 0.23.0,
kubectl 1.30.0 and Helm 3.21.3 on PATH, and use Python 3.12. A virtual environment
is recommended. From the repository root:

```bash
python -m pip install -r hack/dtr-poc/requirements.txt
python hack/dtr-poc/dependencies.py
python hack/dtr-poc/acceptance.py --artifacts .dtr-poc-artifacts/run-1
```

No external PostgreSQL, private application checkout or server credentials are
needed for this command. It provisions synthetic fixtures in its own new Kind
cluster and removes the cluster when it finishes. Use a new result directory on
each run. The initial run needs network access to the public chart and image
registries. The pinned runtime image digests currently target `amd64`.

## Generate tenant values

Use Python 3.12 and install `requirements.txt`. Provide a namespace,
release and tenant slug explicitly; no credentials are accepted by the generator.

```bash
python hack/dtr-poc/tenant_profile.py \
  --namespace umbrella-basyx-poc --release basyx-dtr-poc --tenant poc-a \
  > values-local.yaml
```

This selects the BaSyx bundle, disables the legacy DTR, EDC and data backend,
and assigns tenant-specific names and a namespace-qualified DTR URL. Before
installation, separately provision the tenant's PostgreSQL, database/user/schema
and referenced Secret. The Secret needs `host`, `port`, `dbname`, `user`,
`password`, `jdbc-uri` and `searchPath` keys. Use a dedicated database and
non-superuser role; the role must own its schema so Configuration Service can
initialize it. Never point this profile at a Tractus-X schema.

```bash
python hack/dtr-poc/dependencies.py
helm lint charts/tx-data-provider -f values-local.yaml
helm template basyx-dtr-poc charts/tx-data-provider -n umbrella-basyx-poc \
  -f values-local.yaml --post-renderer python \
  --post-renderer-args hack/dtr-poc/post-render.py
helm install basyx-dtr-poc charts/tx-data-provider -n umbrella-basyx-poc \
  -f values-local.yaml --post-renderer python \
  --post-renderer-args hack/dtr-poc/post-render.py --wait --timeout 5m
```

Pass an explicit reviewed kubeconfig and context for real deployment commands.
The generator never connects to a cluster. `fixtures.py` is test infrastructure
for the newly created Kind cluster, not a production storage provisioner.

## Initialization order

BaSyx 3.15.0 normally uses a post-install initialization Job because its default
database is created by the chart. This bundle requires an existing external
database instead. Its Configuration Service account runs as a pre-install and
pre-upgrade hook at weight -20; the initialization Job follows at weight -10.
Only successful initialization allows Helm to create the DTR Deployment.

The account does not mount a Kubernetes API token. No Kubernetes read permission
is required by Configuration Service. The renderer only removes the unused
`internal-issuer` generated when TLS is disabled; it never rewrites Helm hooks.

Sources: [BaSyx pinned initialization template](https://github.com/eclipse-basyx/charts/blob/basyx-3.15.0/charts/basyx/templates/configuration-service-job.yaml),
[Helm hook lifecycle](https://helm.sh/docs/v3/topics/charts_hooks/).

## Run isolated acceptance

Have Docker, Kind 0.23.0, kubectl 1.30.0, Helm 3.21.3 and Python 3.12 available.
Run from the repository root after dependency resolution:

```bash
python hack/dtr-poc/acceptance.py --artifacts /private/path/new-dtr-results
```

The harness always creates a new uniquely named Kind cluster, passes its own
kubeconfig/context to every Kubernetes and Helm command, and removes that exact
cluster at completion or failure. It uses only `basyx-poc` and
`umbrella-basyx-poc`, with separate storage and runtime-generated credentials.
It refuses a nonempty result directory. Passwords are sent through stdin,
consumed from Secret references and checked for absence from result artifacts.
The temporary kubeconfig is removed with its private temporary directory.

Acceptance covers initialization failure preventing DTR creation; cold start
without DTR restarts; descriptor CRUD, full submodel endpoint metadata and
Asset Link queries; independent values under identical IDs in two tenants;
rejection of one tenant's database credential by the other database, after a
successful control connection; DTR and PostgreSQL Pod replacement persistence;
same-version Helm upgrade/rollback; uninstall and reinstall with unchanged
database Secret, StatefulSet and PVC UIDs; and a default Tractus-X template
comparison against upstream commit `fe1d0cc9d8326cc68dbd6f56433d1baa403d8ebc`.
The comparison permits only three known upstream demo random values, and
validates the two hook labels against the exact new provider chart version.

The GitHub workflow `basyx-dtr-poc.yaml` runs these checks in a hosted runner with
read-only repository permissions, on pull requests and `feat/basyx-*` pushes.
It needs no server credentials or production
secrets. It does not deploy the full Umbrella identity or connector stack.

## Results

`results.json` records versions, tenant image identities, initialization/start
times and check results. `commands.json` records command arguments and exit
codes with temporary kubeconfig paths redacted. `api-events.json` contains only
synthetic descriptors and expected response statuses. Database reports record
schema initialization and least-privilege role checks. No database Secret
manifest or generated password is saved. CI uploads these sanitized artifacts
with seven-day retention.

An overall `PASS` requires both tenants to pass the runtime checks and the
temporary Kind cluster to be removed. The uninstall/reinstall and Helm rollback
checks use the same application/schema version.

## Rollback and limits

Keep the external PostgreSQL, credentials and storage when uninstalling the
application release. Reinstall the same pinned BaSyx version and profile to
recover its own data. Never bootstrap retained storage again. Hook Jobs and
their ServiceAccount can remain after uninstall; the next install/upgrade
recreates them using `before-hook-creation`.

The rollback test uses the same application and schema version. A rollback
across versions requires an independently verified schema recovery plan.
Switching DTR engines is not a Helm rollback or an automatic data migration.

The PoC has private ClusterIP services and no public ingress, OIDC, Keycloak,
ABAC, BMW ECS, HA, migration or production tenant integration. Namespace and
database tests prove independent instances and data; they do not prove network
or authorization isolation. A production rollout still requires the tenant's
network/RBAC boundaries, caller compatibility, data handling and cutover plan.
The default Tractus-X check compares rendered configuration, not a fresh full
Tractus-X runtime or full Umbrella E2E installation.
