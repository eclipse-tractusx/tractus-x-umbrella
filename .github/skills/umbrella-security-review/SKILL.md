---
name: umbrella-security-review
description: 'DevSecOps security review for tractus-x-umbrella. Use when: reviewing a PR for security, hardening Helm charts or Kubernetes manifests, checking securityContext / Pod Security Standards / Kyverno policies, secret leaks and hard-coded credentials, TruffleHog, image pinning and CVE scanning (Trivy), RBAC least privilege, NetworkPolicies, ingress TLS, GitHub Actions hardening (SHA pinning, permissions, script injection, pull_request_target), supply chain and Eclipse DASH license checks.'
argument-hint: 'PR, chart, template or workflow to review'
---

# Umbrella Security Review

The umbrella is a **sandbox / test environment**, but it is copied into real clusters and used as a reference by adopters. Review it as if it would go to production, then label findings that are acceptable *only* because it is a sandbox.

## Procedure

### 1. Scope
```bash
git diff --name-only origin/main...HEAD
```
Classify: chart templates/values, bundle charts, CI workflows, container images (`init-container/`, `simple-data-backend/`), scripts (`dataseeding/`, `hack/`), docs.

### 2. Secrets
- Run a local scan before pushing (CI runs `trufflehog.yml` on PRs and daily):
  ```bash
  trufflehog git file://. --since-commit origin/main --results=verified,unknown
  ```
- Test credentials are allowed **only** in values files, clearly fake, and documented. Never in templates, scripts or images.
- Templates consume credentials via `secretKeyRef` / ExternalSecrets, not plain env values.
- Jobs and scripts must not `echo`/log tokens, passwords or Vault responses (watch `set -x`, `curl -v`, debug output).
- Prefer the External Secrets Operator + Vault path (`values-external-secrets.yaml`) for anything realistic.

### 3. Workload hardening (render first)
```bash
helm template umbrella charts/umbrella -f charts/umbrella/<profile>.yaml > /tmp/render.yaml
kyverno apply .github/kyverno-policies/ --resource /tmp/render.yaml   # if Kyverno CLI is installed
trivy config --helm-values charts/umbrella/<profile>.yaml charts/umbrella   # if Trivy is installed
```
For every new or changed Pod spec (Deployments, StatefulSets, Jobs, CronJobs):
- `runAsNonRoot: true`, `runAsUser` > 0, `allowPrivilegeEscalation: false` (repo Kyverno policies)
- `readOnlyRootFilesystem: true` where possible, `capabilities.drop: [ALL]`, `seccompProfile.type: RuntimeDefault`
- CPU/memory `requests` and `limits` set
- `automountServiceAccountToken: false` unless the API is needed
- No `hostNetwork`, `hostPID`, `hostPath`, privileged containers
- Jobs/CronJobs: `backoffLimit`, `activeDeadlineSeconds`/`ttlSecondsAfterFinished`, `concurrencyPolicy: Forbid` for CronJobs that mutate state

### 4. Images and supply chain
- No `:latest`; pinned tags (digest preferred) and configurable via values.
- Scan images used by the change:
  ```bash
  grep -E '^\s+image:' /tmp/render.yaml | sort -u
  trivy image --severity HIGH,CRITICAL <image>
  ```
- Helm repositories over HTTPS; dependency versions pinned (avoid ranges unless deliberate).
- Java dependencies of `simple-data-backend` must pass Eclipse DASH (`eclipse-dash.yml`, `DEPENDENCIES` file).

### 5. Access and network
- RBAC: no `cluster-admin`, no `*` verbs/resources; prefer namespaced Roles.
- Ingress: TLS available via `values-tls.yaml`; no admin UIs (pgAdmin, Vault, Grafana) exposed without the user opting in.
- Services default to `ClusterIP`.

### 6. GitHub Actions
- Third-party actions pinned to a full commit SHA with a version comment. Find unpinned refs:
  ```bash
  grep -nE 'uses: [^@]+@[^ ]+' .github/workflows/* | grep -vE '@[0-9a-f]{40}'
  ```
- Least-privilege `permissions:` (top-level `contents: read`, widen per job only).
- No `pull_request_target` that checks out or runs PR code.
- No untrusted `${{ github.event.* }}` (titles, bodies, branch names) interpolated directly in `run:`; pass via `env:`.
- Secrets only in jobs that need them; never echoed.

### 7. Report
| Severity | File:line | Finding | Fix | Sandbox-acceptable? |
|---|---|---|---|---|

Order by severity (Critical → Low). Propose concrete diffs for each fix.

## Hard rules
- Real vulnerabilities in released components are reported privately via <https://www.eclipse.org/security/> (see `SECURITY.md`), **not** in public issues or PR comments.
- Never paste secret values into chat, issues, PRs or logs. Reference the location only.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
