---
name: umbrella-release
description: 'Prepare a tractus-x-umbrella release. Use when: aligning the umbrella with a new Tractus-X release (e.g. 26.03), bumping the umbrella chart version, checking that every changed chart is version-bumped so chart-releaser publishes it, updating the release badge and docs, writing release notes, verifying CI (helm-checks, TruffleHog, DASH) is green before a release.'
argument-hint: 'Target Tractus-X release, e.g. 26.09'
---

# Umbrella Release

Charts are published by `.github/workflows/chart-release.yaml` on every push to `main` that touches `charts/**`. It runs `chart-releaser` with `CR_SKIP_EXISTING=true`, so **a chart whose `version:` was not bumped is silently skipped**.

## Procedure

1. **Scope**: list the component versions in the target [Tractus-X release](https://github.com/eclipse-tractusx/tractus-x-release/releases) and compare them with the umbrella dependencies:
   ```bash
   helm dependency list charts/umbrella
   for c in charts/*/; do echo "== $c"; helm dependency list "$c" 2>/dev/null | tail -n +2; done
   ```

2. **Upgrade components** that differ, using the `umbrella-component-upgrade` skill.

3. **Versions**
   - Umbrella chart `version:` follows the release scheme already used in `charts/umbrella/Chart.yaml` (e.g. `26.03.00` → `<YY.MM>.<patch>`).
   - Every chart changed since the last release has a new `version:`:
     ```bash
     git diff --name-only <last-release-tag>..HEAD -- charts/ | cut -d/ -f2 | sort -u
     ```
   - Run `./.github/skills/umbrella-helm-validation/scripts/check-dependency-versions.sh`.

4. **Docs**
   - Release badge in `README.md`.
   - "Since Release X" statements and the default scenario in `docs/README.md`.
   - Install reference and component tables in `docs/user/common/installation.md`.
   - Breaking changes in `docs/admin/migration-guide.md`.

5. **Quality gates** (all must be green on the release PR)
   - `helm-checks.yaml` (ct lint + KinD installs of `charts/values-test-*.yaml`)
   - `trufflehog.yml`, `eclipse-dash.yml`, `java-ci.yml` (if `simple-data-backend` changed)
   - Runtime check of the default profile with the `umbrella-deploy-verify` skill
   - Security pass with the `umbrella-security-review` skill

6. **Release notes**: components and versions, new/removed profiles or values, breaking changes and migration steps, known issues.

7. **After merge**: confirm the new chart versions appear on the GitHub Releases page / Helm index. If a chart is missing, its version was probably not bumped.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
