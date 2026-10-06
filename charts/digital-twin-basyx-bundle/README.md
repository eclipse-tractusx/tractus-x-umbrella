<!-- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Optional BaSyx Digital Twin Bundle

This PoC bundle uses official BaSyx chart 3.15.0 and pins DTR and Configuration
Service 1.1.0 images by digest. The `tx-data-provider` chart continues to select
Tractus-X DTR by default. Enable the BaSyx bundle and explicitly disable the
legacy bundle to evaluate an independent BaSyx instance.

The profile is DTR-only: no identity stack, EDC, data backend, public ingress,
Gateway, TLS certificate or authentication is provisioned. Other BaSyx
components stay disabled. The current image digests target `amd64`.

## Self-contained acceptance

For a disposable installation with generated test databases and synthetic
descriptors, use the [tenant acceptance quick start](../../hack/dtr-poc/README.md).
The harness creates its own Kind cluster and needs no existing tenant or private
application. It is the shortest path for a contributor to reproduce this PoC.

## Install with an existing independent database

From the repository root, use Python 3.12 with the test requirements installed:

```bash
python -m pip install -r hack/dtr-poc/requirements.txt
python hack/dtr-poc/dependencies.py
python hack/dtr-poc/tenant_profile.py \
  --namespace umbrella-basyx-poc --release basyx-dtr-poc --tenant poc-a \
  > values-local.yaml
```

This assigns tenant-specific resource names and a namespace-qualified Registry
URL. Create the reviewed namespace, independent PostgreSQL instance, retained
storage, database, non-superuser role, owned schema and referenced database
Secret before installing. PostgreSQL 18.4 was used in acceptance; other versions
are not covered by this test. See the
[database Secret contract](../../hack/dtr-poc/README.md#generate-tenant-values).
Keep credentials out of values files, command arguments, logs and Git.

Render and review before applying. Replace the kubeconfig and context arguments
with your explicitly reviewed test target:

```bash
helm lint charts/tx-data-provider -f values-local.yaml
helm template basyx-dtr-poc charts/tx-data-provider -n umbrella-basyx-poc \
  -f values-local.yaml --post-renderer python \
  --post-renderer-args hack/dtr-poc/post-render.py
helm install basyx-dtr-poc charts/tx-data-provider -n umbrella-basyx-poc \
  --kubeconfig /path/to/test-kubeconfig --kube-context reviewed-test-context \
  -f values-local.yaml --post-renderer python \
  --post-renderer-args hack/dtr-poc/post-render.py --wait --timeout 5m
```

Use the same values and post-renderer when upgrading. Official BaSyx chart
3.15.0 emits an unused `internal-issuer` with TLS disabled. The delivered
post-renderer removes only this Issuer; it does not modify initialization hooks
or other objects. This avoids requiring cert-manager for the isolated profile.

## Startup order

The external database and Secret must already exist. Configuration Service's
ServiceAccount runs as a `pre-install,pre-upgrade` hook at weight -20, before
the initialization Job at weight -10. Helm creates the DTR only after successful
initialization. Missing prerequisites or selection of both DTR bundles cause
an early template failure.

## API contract and limits

Use `/digital-twin-registry` for the BaSyx API base, including when overriding
`registryUrl`. Do not append the legacy `/api/v3` path. Synthetic acceptance
covers Base64URL identifiers, descriptor CRUD, complete Submodel endpoint
metadata and Asset Link lookups. Error response envelopes differ between DTR
implementations; this is not a claim of complete API equivalence.

Registry descriptors point to a Submodel data service. This chart does not
provide that service or validate EDC negotiation/data delivery. The bulk dataset
importer, production tenant integration, ABAC, OIDC, Keycloak, BMW ECS, HA,
performance, network isolation and data migration are outside this profile.

## Rollback and retained data

Roll back an application revision using an explicit test kubeconfig/context:

```bash
helm rollback basyx-dtr-poc 1 -n umbrella-basyx-poc \
  --kubeconfig /path/to/test-kubeconfig --kube-context reviewed-test-context \
  --wait --timeout 5m
```

The acceptance rollback uses the same application/schema version. Downgrading
versions requires a separately verified database backup and recovery plan.

Uninstall the application while retaining the external database, Secret and
storage. Reinstall the same pinned version and profile to read the retained
data. Never bootstrap retained PostgreSQL storage again. Hook resources may
remain after uninstall; the next install/upgrade recreates them through
`before-hook-creation`. Switching DTR engines is not a Helm rollback.
