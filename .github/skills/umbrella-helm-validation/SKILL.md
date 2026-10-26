---
name: umbrella-helm-validation
description: 'Validate Helm chart changes in tractus-x-umbrella before a PR. Use when: changing charts/umbrella or any bundle chart, editing templates or values, bumping chart versions, checking file:// dependency version sync, running helm lint / helm template / ct lint, reproducing the helm-checks CI workflow locally, reviewing a chart PR.'
argument-hint: 'Chart(s) or profile(s) to validate, e.g. charts/tx-data-provider'
---

# Umbrella Helm Validation

Reproduce what CI (`.github/workflows/helm-checks.yaml`) checks, plus the umbrella-specific consistency rules CI does not catch.

## When to Use

- Any change under `charts/**`
- Before opening or approving a chart PR
- After running `./hack/helm-dependencies.bash` and something looks off

## Procedure

1. **Identify the change set**
   ```bash
   git diff --name-only origin/main...HEAD -- charts/
   ```
   Map every changed file to its chart (`charts/<chart>/`) and to every chart that depends on it via `file://` (bundle → `tx-data-provider` / `decentralized-identity-connector` → `umbrella`).

2. **Version bump rules**
   - Every changed chart needs a new `version:` in its `Chart.yaml`. `ct lint` enforces a version increment, and `chart-release.yaml` runs with `CR_SKIP_EXISTING=true`, so an un-bumped chart is **silently not released**.
   - Every parent that consumes it via `file://` must reference the new version (and get its own bump).
   - Run the consistency check:
     ```bash
     ./.github/skills/umbrella-helm-validation/scripts/check-dependency-versions.sh
     ```

3. **Refresh dependencies** (order matters because of `file://` chains):
   ```bash
   ./hack/helm-dependencies.bash
   ```
   Never commit or hand-edit content under `charts/*/charts/`.

4. **Lint**
   ```bash
   helm lint charts/<chart>
   helm lint charts/umbrella -f charts/umbrella/<profile>.yaml
   ct lint --validate-maintainers=false --target-branch main   # if chart-testing is installed
   ```

5. **Render every affected profile** and inspect the diff, not just the exit code:
   ```bash
   for f in charts/umbrella/values-adopter-*.yaml charts/values-test-*.yaml; do
     helm template umbrella charts/umbrella -f "$f" > "/tmp/render-$(basename "$f" .yaml).yaml" || echo "FAILED: $f"
   done
   ```
   Compare against `origin/main` renders when the change should be behavior-neutral.

6. **Schema validation** (optional, if installed):
   ```bash
   kubeconform -strict -ignore-missing-schemas -summary /tmp/render-*.yaml
   kubectl apply --dry-run=client -f /tmp/render-<profile>.yaml
   ```

7. **Composability checks** on the rendered output:
   - New resources are gated behind an `*.enabled` flag defaulting to `false`.
   - Disabling the flag removes the resource: `helm template ... --set <path>.enabled=false --show-only templates/<file>.yaml` must error with "could not find template".
   - No hard-coded hostnames, namespaces, release names or secrets — use values and `{{ .Release.Name }}` / helpers.

8. **Docs and headers**: user-visible values or behavior changed → update `docs/` and the chart `README.md` (and `README.md.gotmpl` where present). New files carry the SPDX header.

## Output

Report per chart: version bump OK/missing, dependency sync OK/mismatch, lint result, render result per profile, notable diff, docs updated yes/no.

## Resources

- [check-dependency-versions.sh](./scripts/check-dependency-versions.sh): verifies every `file://` dependency version equals the referenced chart's `version:`.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
