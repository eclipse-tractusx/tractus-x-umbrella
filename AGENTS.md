# AGENTS.md

> Context file for AI agents (GitHub Copilot, Claude, Cursor, etc.) working on this repository.
> Read this **before** making changes so you understand the layout, conventions and the moving parts of the project.

## 1. What this repository is

**Eclipse Tractus-X Umbrella** is an **umbrella Helm chart** that spins up a complete [Catena-X](https://catena-x.net/en/) automotive dataspace network using [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) open-source components.

It is **not** an application — it is **infrastructure-as-code** built on top of:

- **Helm 3.12+** charts (mostly aggregated as dependencies of other Tractus-X charts).
- **Kubernetes** (>= 1.24.x), typically deployed locally on **Minikube** (Linux/macOS preferred).
- A small amount of supporting Java code ([simple-data-backend](simple-data-backend)) and Python tooling ([dataseeding](dataseeding)).

Main goals:

1. **End-to-end testing** of Catena-X services.
2. **Sandbox / developer environments** for evaluating components.
3. **Reproducible setups** for contributors of the Tractus-X projects.

Current overarching release: **Tractus-X Release 25.12**.

---

## 2. Top-level layout

```
tractus-x-umbrella/
├── charts/                  ← ★ MOST IMPORTANT FOLDER (Helm charts live here)
├── docs/                    ← User & admin documentation, architecture, guides
├── dataseeding/             ← Python tooling for seeding Vault secrets / test data
├── hack/                    ← Helper bash scripts (e.g. helm-dependencies.bash)
├── init-container/          ← Dockerfile + IAM init resources for centralidp
├── simple-data-backend/     ← Tiny Spring Boot backend used as a data provider in tests
├── .act/                    ← Sample events for running GitHub workflows locally with `act`
├── .github/                 ← GitHub Actions workflows, issue templates, CODEOWNERS
├── .tractusx                ← Tractus-X release metadata
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── NOTICE.md
├── LICENSE                  ← Apache-2.0 (code)
└── LICENSE_non-code         ← CC-BY-4.0 (docs)
```

---

## 3. `charts/` — the heart of the repo

`charts/` contains the **umbrella chart** plus the **capability bundles** it depends on, all wired together via Helm `file://` dependencies.

```
charts/
├── umbrella/                          ← ★ THE MAIN CHART (entry point)
│   ├── Chart.yaml                     ← Aggregates all dependencies (portal, IAM, EDC bundles, BPDM, ...)
│   ├── values.yaml                    ← Main / default values
│   ├── values-adopter-data-exchange.yaml
│   ├── values-adopter-data-exchange-observability.yaml
│   ├── values-adopter-decentralized-identityhub.yaml
│   ├── values-adopter-portal.yaml
│   ├── values-external-secrets.yaml
│   ├── values-tls.yaml
│   ├── cluster-issuer.yaml
│   ├── templates/                     ← Glue templates (post-install jobs, fake secrets, smtp, ...)
│   ├── resources/                     ← Static resources (e.g. grafana-dashboard.json)
│   └── charts/                        ← Resolved Helm dependencies (do NOT edit by hand)
│
├── dataspace-connector-bundle/        ← Tractus-X EDC connector + Postgres + Vault
├── identity-and-trust-bundle/         ← SSI DIM wallet stub (identity & trust services)
├── digital-twin-bundle/               ← Digital Twin Registry + Postgres
├── data-persistence-layer-bundle/     ← simple-data-backend
├── decentralized-identity-connector/  ← Bundle for the decentralized identity flow
├── tx-data-provider/                  ← Composite chart pulling several bundles together
│                                         (re-used by the umbrella as dataconsumerOne / dataconsumerTwo / tx-data-provider)
├── tractusx-issuerservice/            ← Issuer service + pgadmin4 + postgres + vault
├── simple-data-backend/               ← Helm chart for the Spring Boot backend
├── umbrella-infrastructure/           ← Cluster-level infra (ingress, cert-manager, etc.)
│
├── values-test-data-exchange.yaml     ← CI test value sets used by GH Actions
├── values-test-iam-init-container-1.yaml
├── values-test-iam-init-container-2.yaml
├── values-test-shared-services-1.yaml
└── values-test-shared-services-2.yaml
```

### 3.1 The umbrella chart

`charts/umbrella/` is **the entry point** for any deployment. It:

- Declares **all upstream Tractus-X components** as Helm dependencies in `Chart.yaml` (portal, centralidp, sharedidp, bpdm, ssi-credential-issuer, semantic-hub, discovery-finder, bpn-discovery, sd-factory, pgadmin4, ...).
- Pulls the **local bundles** under `charts/` via `repository: file://../<bundle>`.
- Exposes per-component toggles through `*.enabled` flags so subsets can be turned on/off.
- Provides several **`values-adopter-*.yaml`** profiles for typical scenarios:
  - `values-adopter-data-exchange.yaml` — data exchange flow (EDC + DTR + BPDM).
  - `values-adopter-data-exchange-observability.yaml` — same + Prometheus/Grafana.
  - `values-adopter-decentralized-identityhub.yaml` — decentralized identity hub scenario.
  - `values-adopter-portal.yaml` — portal-focused setup.
  - `values-external-secrets.yaml` — uses External Secrets Operator instead of fake secrets.
  - `values-tls.yaml` — TLS / ingress-with-certs configuration.

Typical install:

```bash
helm install umbrella charts/umbrella \
  -f charts/umbrella/values-adopter-data-exchange.yaml
```

### 3.2 Capability bundles

Each *bundle* is a small Helm chart that groups one Tractus-X capability with its required sidecars (DB, Vault, …). Bundles are versioned independently (see their `Chart.yaml`).

| Bundle | Purpose | Key dependencies |
|---|---|---|
| `dataspace-connector-bundle` | Tractus-X EDC connector | `tractusx-connector`, `postgresql`, `vault` |
| `identity-and-trust-bundle` | Identity / SSI services | `ssi-dim-wallet-stub` |
| `digital-twin-bundle` | Digital Twin Registry | `digital-twin-registry`, `postgresql` |
| `data-persistence-layer-bundle` | Simple data backend | `simple-data-backend` |
| `decentralized-identity-connector` | Decentralized identity setup | composes `tx-data-provider` |
| `tx-data-provider` | Composite provider/consumer | `digital-twin-bundle`, `data-persistence-layer-bundle`, `dataspace-connector-bundle` |
| `tractusx-issuerservice` | Issuer service stack | `issuerservice`, `postgres`, `vault`, `pgadmin4` |
| `simple-data-backend` | Spring Boot backend chart | – |
| `umbrella-infrastructure` | Cluster infra prerequisites | – |

> ⚠️ **Bundle versions are referenced from `umbrella/Chart.yaml` via `file://` paths.**
> If you bump a bundle’s `version:` in its `Chart.yaml`, you must also update the matching `version:` entry in `charts/umbrella/Chart.yaml` (and re-run dependency update).

---

## 4. Common workflows for an AI agent

### 4.1 Updating Helm dependencies

Use the helper script — it walks all charts in the correct order:

```bash
./hack/helm-dependencies.bash
```

This is preferred over running `helm dependency update` manually because of the inter-chart `file://` dependencies.

### 4.2 Rendering / linting a chart

```bash
helm lint charts/umbrella -f charts/umbrella/values-adopter-data-exchange.yaml
helm template umbrella charts/umbrella -f charts/umbrella/values-adopter-data-exchange.yaml
```

### 4.3 Local install (Minikube)

See [`docs/user/linux/README.md`](docs/user/linux/README.md) (preferred), [`docs/user/mac/README.md`](docs/user/mac/README.md), or [`docs/user/windows/README.md`](docs/user/windows/README.md).

### 4.4 Running GitHub workflows locally

Use [`act`](https://github.com/nektos/act) with the sample events under `.act/`:

```bash
act -e .act/pr_event.json pull_request
```

### 4.5 Documentation

All user-facing docs live under [`docs/`](docs/). Start at [`docs/README.md`](docs/README.md). Always update docs when you change behavior or add a value flag that is user-visible.

---

## 5. Conventions and rules

### 5.1 File headers / licensing

Every source file (YAML, Java, Python, Bash, …) **must** carry the Eclipse SPDX header:

```yaml
# #############################################################################
# Copyright (c) <year> Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# ... (standard Apache-2.0 disclaimer) ...
#
# SPDX-License-Identifier: Apache-2.0
# #############################################################################
```

- **Code** → `Apache-2.0`
- **Docs / markdown / images** → `CC-BY-4.0` (see `LICENSE_non-code`)

Preserve existing copyright lines when editing; add a new copyright line only when introducing substantial new content.

### 5.2 Chart conventions

- Bump the `version:` in a bundle's `Chart.yaml` whenever its templates or values change in a way that affects consumers, and update the matching dependency version in `charts/umbrella/Chart.yaml`.
- Keep `appVersion`, when present, aligned with the upstream Tractus-X release.
- Do **not** hand-edit anything under `charts/*/charts/` — that directory is populated by `helm dependency update`.
- Prefer adding new behavior behind a `*.enabled` flag (default `false`) to avoid breaking existing profiles.
- When introducing a new component, also wire it into the relevant `values-adopter-*.yaml` profile if it belongs to that scenario.

### 5.3 Commits & PRs

- Conventional, descriptive commit messages.
- Sign-off (`Signed-off-by:`) is required per the Eclipse DCO — see [`CONTRIBUTING.md`](CONTRIBUTING.md).
- CI runs `helm lint`, template rendering, and integration tests using the `charts/values-test-*.yaml` files; keep those green.

### 5.4 Secrets

- The default profile uses **fake external secrets** (templates `fake-external-secrets.yaml`, `fake-secretstore.yaml`) so the chart can run without any Vault.
- For realistic setups, use `values-external-secrets.yaml` together with the Vault setup under [`dataseeding/`](dataseeding/) and the docs at [`docs/user/common/secrets/`](docs/user/common/secrets/).
- **Never** commit real credentials or production-like secret values.

---

## 6. Supporting components

### `simple-data-backend/`
Spring Boot (Java) backend used as a sample data provider in test pipelines.
- Build with Maven (`mvn package` inside that folder).
- A Helm chart wrapper lives at `charts/simple-data-backend/`.

### `dataseeding/`
Python utility ([`vault-secrets-setup.py`](dataseeding/vault-secrets-setup.py)) that seeds HashiCorp Vault with secrets required by the connectors / issuer service. Requirements in `dataseeding/requirements.txt`.

### `init-container/`
Dockerfile + IAM resources for the centralidp init container (Keycloak realm setup, etc.).

### `hack/`
Bash helpers — currently `helm-dependencies.bash` to refresh all chart deps in the right order.

---

## 7. Quick-reference cheat sheet for agents

| I want to… | Look here |
|---|---|
| Change which components are deployed | `charts/umbrella/values.yaml` or a `values-adopter-*.yaml` |
| Add a new upstream Tractus-X component | `charts/umbrella/Chart.yaml` (dependencies) + values |
| Modify a bundle (EDC, DTR, IAM, …) | `charts/<bundle>/` then bump version & sync in umbrella |
| Update sub-chart versions after edits | `./hack/helm-dependencies.bash` |
| Render manifests locally | `helm template umbrella charts/umbrella -f <values>` |
| Find user-facing docs | `docs/README.md` |
| Inspect CI test value sets | `charts/values-test-*.yaml` |
| Configure secrets management | `docs/user/common/secrets/` + `dataseeding/` |
| Add static resources (dashboards, etc.) | `charts/umbrella/resources/` |
| Glue logic at install time | `charts/umbrella/templates/post-install-*.yaml` |

---

## 8. Things to avoid

- ❌ Editing files under `charts/*/charts/` (auto-generated by Helm).
- ❌ Bumping a bundle version without updating `charts/umbrella/Chart.yaml`.
- ❌ Hard-coding secrets, hostnames, or environment-specific values without a `values.yaml` knob.
- ❌ Removing `*.enabled` conditions — they keep the chart composable.
- ❌ Introducing new top-level folders without updating this `AGENTS.md` and [`docs/README.md`](docs/README.md).
- ❌ Stripping or altering existing SPDX / copyright headers.

---

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
