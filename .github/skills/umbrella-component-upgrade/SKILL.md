---
name: umbrella-component-upgrade
description: 'Upgrade a Tractus-X or third-party component in tractus-x-umbrella. Use when: bumping EDC / tractusx-connector, IdentityHub, IssuerService, DTR, portal, centralidp, sharedidp, BPDM, BDRS, semantic-hub, discovery, ssi-dim-wallet-stub, postgresql, vault, cert-manager, observability charts; aligning with a new Tractus-X release; diffing upstream values.yaml between versions; propagating bundle versions through tx-data-provider and the umbrella chart; rollback.'
argument-hint: 'Component and target version, e.g. tractusx-connector 0.13.0'
---

# Umbrella Component Upgrade

Based on `docs/admin/upgrade-components.md`, extended with the checks that usually go wrong.

## Procedure

1. **Pick the target version**
   - Tractus-X components: use the chart version listed in the [Tractus-X release](https://github.com/eclipse-tractusx/tractus-x-release/releases) the umbrella is aligning to. Don't mix versions across releases unless there's a documented reason.
   - Read the upstream CHANGELOG and migration notes for every version in between.

2. **Find where the component is wired**
   ```bash
   grep -rn --include=Chart.yaml -A3 "name: <component>" charts/
   ```
   - Direct dependency of `charts/umbrella` → change only the umbrella.
   - Inside a bundle (`dataspace-connector-bundle`, `digital-twin-bundle`, `decentralized-identity-connector`, …) → follow the chain: bundle → `tx-data-provider` / `decentralized-identity-connector` → `umbrella`.

3. **Diff upstream defaults** (catch renamed or removed keys):
   ```bash
   helm repo update
   helm show values <repo>/<chart> --version <old> > /tmp/old.yaml
   helm show values <repo>/<chart> --version <new> > /tmp/new.yaml
   diff -u /tmp/old.yaml /tmp/new.yaml
   helm show chart <repo>/<chart> --version <new>   # appVersion, sub-dependencies
   ```
   Then grep every overridden key in the umbrella/bundle values and all `values-adopter-*.yaml` / `charts/values-test-*.yaml` to make sure it still exists.

4. **Apply**
   - Update the dependency `version:`.
   - Bump the chart's own `version:` (semver: patch = config fix, minor = new component version/feature, major = breaking values change) and propagate up the chain.
   - Adjust values overrides. Keep image tags configurable.

5. **Validate**: run the `umbrella-helm-validation` skill (dependency sync script, lint, render all profiles).

6. **Runtime check**: run the `umbrella-deploy-verify` skill for every profile that enables the component (at minimum the default decentralized IdentityHub profile and the affected CI value set).

7. **Security**: scan the new images (`trivy image`) and note fixed/new CVEs in the PR description.

8. **Docs**: update `docs/user/common/installation.md` (component/version tables), any guide that shows changed endpoints or steps, and `docs/admin/migration-guide.md` for breaking changes.

## Rollback
1. Revert the version changes in all affected `Chart.yaml` files.
2. `./hack/helm-dependencies.bash`
3. `helm upgrade` (or reinstall) with the previous chart version. Databases may have been migrated by the new version; check upstream notes before downgrading, and recreate test data if needed.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
