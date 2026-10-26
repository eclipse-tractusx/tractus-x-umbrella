---
name: umbrella-test-session
description: 'Spin up fast, isolated, throw-away deployments of parts of the umbrella to test a PR or a change, and compare two versions. Use when: testing new functionality from a pull request, deploying only one bundle or a reduced umbrella, running main and a PR side by side, comparing rendered manifests between git refs, comparing deployed values, images or behavior of two sessions, quick before/after checks.'
argument-hint: 'What to test or compare, e.g. "PR 440 dataspace-connector-bundle vs main"'
---

# Umbrella Test Session

Fast feedback with the smallest deployment that proves the point. Every session is one namespace labelled `umbrella-guardian/session=<name>`, so sessions never touch each other or a normal `umbrella` install, and cleanup is one command.

Helper: [scripts/session.sh](./scripts/session.sh) (run `session.sh help`).

## 1. Pick the cheapest test that answers the question

| Question | Do this | Cluster needed |
|---|---|---|
| "What does this PR change in the manifests?" | `diff-render` | No |
| "Does the changed bundle start and work?" | `up` the bundle alone | Yes |
| "Does it still work inside a participant / the umbrella?" | `up` `tx-data-provider`, `decentralized-identity-connector` or a reduced `umbrella` | Yes |
| "Is it different/better than main at runtime?" | two sessions + `diff-sessions` | Yes |

Always start with `diff-render`: it is seconds, needs no cluster, and often answers the question alone. Deploy only what the change touches; prefer a single bundle over the whole umbrella (see `docs/user/common/guides/hausanschluss-bundles.md`).

## 2. Get the PR sources

```bash
S=.github/skills/umbrella-test-session/scripts/session.sh
$S pr 440                # fetches pull/440/head -> ref origin/pr/440, worktree path on stdout
```

Worktrees live in `$UMBRELLA_SESSION_DIR` (default `$TMPDIR/umbrella-sessions`) and are reused on the next run. Your own checkout and branch stay untouched.

**PR code is untrusted.** The helper only runs `helm` on it; do not run the PR's own scripts (`hack/`, `dataseeding/`, workflows) without reading them first.

## 3. Compare rendered manifests (no cluster)

```bash
$S diff-render origin/main origin/pr/440 dataspace-connector-bundle
$S diff-render origin/main . umbrella -- -f charts/umbrella/values-adopter-decentralized-identityhub.yaml
```

- `.` means your working tree (uncommitted changes included).
- Helm args after `--` resolve inside each ref, so each side uses its own values file.
- Uses `dyff` if installed, else `diff -u`. Rendered files are kept for `grep`.
- **Ignore noise**: randomly generated secrets, passwords, certificates and checksum annotations change on every render.

## 4. Deploy a session

Requires a **local** cluster (minikube, kind, k3d, Docker Desktop, Rancher Desktop, OrbStack). The helper refuses any other kube context unless `UMBRELLA_SESSION_CONTEXT=<context>` is set: never deploy test sessions to shared clusters without the user's explicit OK. For cluster setup see the `umbrella-deploy-verify` skill.

```bash
$S up pr440 dataspace-connector-bundle --src "$($S pr 440)"
$S up main  dataspace-connector-bundle            # baseline from your checkout
$S status pr440                                    # waits for pods, shows pods, jobs, ingress, images
```

- Only the chart's `file://` chain is refreshed (bundles first, then parents), not every chart in the repo.
- The release name defaults to the chart folder (`umbrella`, `tx-data-provider`, ...) so values that reference release-prefixed service names keep working, and two sessions differ only by namespace.
- Reduced umbrella: pass a profile plus `--set <component>.enabled=false` for everything the test does not need.
- **Side by side caveats**: ingress hosts are fixed in values, so two sessions of the same chart collide on ingress. Override the hosts for one session (`--set ...hostname=pr440-...`), or disable ingress and use `kubectl port-forward`. Cluster-scoped resources (cert-manager issuers, CRDs, ClusterRoles) are shared; deploy those once.

## 5. Compare two sessions

```bash
$S diff-sessions main pr440
```

Shows the difference in user-supplied values, container images and the full manifests (namespace normalized). For behavior, run the same check against both sessions (e.g. a `curl` via `kubectl port-forward`, or the relevant Bruno folder) and put the results next to each other.

## 6. Report

Use this layout:

| | `main` | `pr440` |
|---|---|---|
| Source | ref + short SHA | ref + short SHA |
| Pods / jobs | Ready x/y, jobs completed | ... |
| Images | ... | ... |
| Functional check | result | result |

Then state the **verdict** (works / regression / improvement) and what you would recommend. If the comparison reveals that the PR's approach is questionable, challenge it as described in the agent's "Challenge and recommend" rules.

## 7. Clean up (ask first)

```bash
$S list
$S down pr440 --yes            # uninstalls and deletes the session namespace, PVCs included
git worktree remove <path printed by "$S pr 440">
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
