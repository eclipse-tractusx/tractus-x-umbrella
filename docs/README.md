# Tractus-X Umbrella — Documentation

Spin up a complete [Catena-X](https://catena-x.net/en/) dataspace locally for testing,
development or sandbox usage, on top of [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx)
open-source components.

> [!TIP]
> **New here?** Jump straight to the **[Quickstart](user/quickstart.md)** — it takes
> you from an empty machine to a working dataspace using the **recommended profile
> (Decentralized IdentityHub)** in under 10 commands.

---

## 1. The recommended path

Since Release 25.12 the **decentralized identity** flow (DIDs + per-participant
IdentityHub + IssuerService) is the **default scenario** for the umbrella chart. It
replaces the older CX-IAM + central wallet stub setup and matches where the Catena-X
ecosystem is heading.

| What | Where |
|------|-------|
| **Profile** | [`charts/umbrella/values-adopter-decentralized-identityhub.yaml`](../charts/umbrella/values-adopter-decentralized-identityhub.yaml) |
| **End-to-end walkthrough** | [Quickstart](user/quickstart.md) |
| **What gets deployed** | [Data Exchange with Decentralized IdentityHub](user/common/guides/data-exchange-identityhub.md) |
| **Credential issuance flow** | [Issuance guide](user/common/guides/data-exchange/issuance.md) |
| **API tests (Bruno)** | [Bruno collection](common/api/README.md) |

> The legacy centralized flow (CX-IAM + `ssi-dim-wallet-stub`) is still available via
> `values-adopter-data-exchange.yaml`. It is kept for backwards compatibility — see
> [Other scenarios](#3-other-scenarios) below.

---

## 2. Set up your cluster (OS-specific)

The umbrella chart itself is OS-agnostic. These pages cover **only the
cluster + DNS setup** for each platform:

- 🐧 **[Linux](user/linux/README.md)** — preferred platform (Minikube + ingress-dns)
- 🍎 **[macOS](user/mac/README.md)** — Docker Desktop + Minikube, or Lima + K3s
- 🪟 **[Windows](user/windows/README.md)** — Docker Desktop, Hyper-V, or WSL2

Once your cluster + DNS are ready, follow the [Quickstart](user/quickstart.md) — the
`helm install` command and all the application-level steps are the **same across OSes**.

> Looking for the full install reference (all profiles, `--set` flags, released chart, uninstall)?
> See [Installation Reference](user/common/installation.md).

---

## 3. Other scenarios

Use these only if the default (Decentralized IdentityHub) does not match what you need.

| Profile | When to use it |
|---------|----------------|
| `values-adopter-data-exchange.yaml` | Legacy centralized data exchange (CX-IAM + central wallet stub) |
| `values-adopter-data-exchange-observability.yaml` | Same as above + Prometheus / Grafana / Loki / Jaeger |
| `values-adopter-portal.yaml` | Portal-only setup (UI, BPDM, onboarding) |
| `values-external-secrets.yaml` | Replace fake secrets with HashiCorp Vault + ESO |
| `values-tls.yaml` | TLS / ingress with certificates (cert-manager) |

See the per-profile guides under [user/common/guides/](user/common/guides/).

---

## 4. Working guides (post-install)

Once the chart is deployed, these are the things you'll actually *do* with it:

- 📤 [Provide data as a Data Provider](user/common/guides/data-exchange/provide-data.md)
- 📥 [Consume data as a Data Consumer](user/common/guides/data-exchange/consume-data.md)
- 🪪 [Issue verifiable credentials](user/common/guides/data-exchange/issuance.md)
- 🖥️ [Use the Portal UI](user/common/guides/portal-usage.md)
- 🗄️ [Access the databases (pgAdmin)](user/common/guides/database-access.md)
- 📈 [Observability (Prometheus, Grafana, Loki, Jaeger)](user/common/guides/observability/observability.md)
- 🧩 [Run a single capability bundle (Hausanschluss)](user/common/guides/hausanschluss-bundles.md)
- 🔐 [External Secrets Operator + Vault](user/common/guides/external-secrets.md)

---

## 5. Reference & advanced topics

<details>
<summary><b>Secrets management (Vault, ESO)</b></summary>

The default install uses **fake external secrets** so the chart runs with zero extra
setup. The links below are only relevant if you want a realistic secrets backend.

- [Overview](user/common/secrets/README.md) ·
  [Deployment](user/common/secrets/deployment.md) ·
  [Vault setup](user/common/secrets/vault-setup.md) ·
  [Configuration](user/common/secrets/configuration.md) ·
  [Connected services](user/common/secrets/connected-services.md) ·
  [Troubleshooting](user/common/secrets/troubleshooting.md)
</details>

<details>
<summary><b>Troubleshooting</b></summary>

- [Common issues](user/common/troubleshooting/README.md) (DNS, CoreDNS, search-domain inheritance, …)
</details>

<details>
<summary><b>Administration</b></summary>

- [Upgrade components](admin/upgrade-components.md)
- [Migration notes](admin/migration-guide.md)
</details>

<details>
<summary><b>Architecture & concepts</b></summary>

- [Architecture Decision Records](common/architecture/decision-records/)
- [Concept: Hausanschluss bundles](common/concept/solution-design-hausanschluss-bundle.md)
- [Concept: Cloud-ready infrastructure automation](common/concept/solution-design-cloud-ready-infrastructure-automation.md)
- [ADR: Secret management](common/concept/adr-secret-management.md)
- [Repository context for AI agents (AGENTS.md)](../AGENTS.md)
</details>

<details>
<summary><b>Historical / archive</b></summary>

Kept for traceability; **not relevant for current deployments**.

- [Legacy per-OS documentation](archive/legacy-per-os/)
</details>

---

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
