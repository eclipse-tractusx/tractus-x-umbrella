#!/usr/bin/env bash
# #############################################################################
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
# #############################################################################

# Fast, isolated umbrella test sessions: one labelled namespace per session on a local cluster.
# Kept bash 3.2 compatible (macOS default shell).
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SESSION_DIR="${UMBRELLA_SESSION_DIR:-${TMPDIR:-/tmp}/umbrella-sessions}"
SESSION_DIR="${SESSION_DIR%/}"
REMOTE="${UMBRELLA_REMOTE:-origin}"
TIMEOUT="${UMBRELLA_SESSION_TIMEOUT:-15m}"
LABEL="umbrella-guardian/session"
CTX=""
DONE_DEPS=" "

usage() {
  cat <<'EOF'
Usage: session.sh <command> [args]

  pr <number>                          Fetch a PR into a reusable worktree and print its path
  up <session> <chart> [options] [-- helm args]
        --src DIR                      Chart sources (default: this checkout; use the path from `pr`)
        --release NAME                 Release name (default: chart folder name, e.g. umbrella)
        --namespace NS                 Namespace (default: ug-<session>)
  status <session>                     Wait for pods, then show pods, jobs, ingress and images
  list                                 List sessions and session worktrees
  diff-render <refA> <refB> <chart> [-- helm args]
                                       Render a chart at two git refs ("." = working tree) and diff
  diff-sessions <sessionA> <sessionB>  Diff deployed values, manifests and images of two sessions
  down <session> --yes                 Uninstall the session and delete its namespace

<chart> is a folder under charts/ (umbrella, tx-data-provider, dataspace-connector-bundle, ...).
Helm args after -- are passed through and resolved relative to the chart sources, e.g.
  -- -f charts/umbrella/values-adopter-decentralized-identityhub.yaml

Environment: UMBRELLA_SESSION_DIR, UMBRELLA_REMOTE (default origin), UMBRELLA_SESSION_TIMEOUT (default 15m),
UMBRELLA_SESSION_CONTEXT (required to use a kube context that is not a known local cluster).
EOF
  exit "${1:-0}"
}

die() { echo "error: $*" >&2; exit 1; }

check_name() {
  [[ "$1" =~ ^[a-z0-9]([-a-z0-9]{0,28}[a-z0-9])?$ ]] || die "session name must be a lowercase DNS label, max 30 chars: '$1'"
}

use_cluster() {
  CTX="$(kubectl config current-context 2>/dev/null)" || die "no current kubectl context"
  case "$CTX" in
    minikube|kind-*|k3d-*|docker-desktop|rancher-desktop|orbstack|colima*) ;;
    *)
      [[ "${UMBRELLA_SESSION_CONTEXT:-}" == "$CTX" ]] ||
        die "context '$CTX' is not a known local cluster. Switch to minikube/kind, or set UMBRELLA_SESSION_CONTEXT=$CTX to confirm."
      ;;
  esac
}

k() { kubectl --context "$CTX" "$@"; }
h() { helm --kube-context "$CTX" "$@"; }

session_ns() {
  local ns
  ns="$(k get namespaces -l "$LABEL=$1" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  [[ -n "$ns" ]] || die "no session '$1' (see: session.sh list)"
  echo "$ns"
}

session_release() {
  h list -n "$1" -q | head -n 1
}

checkout_ref() {
  if [[ -d "$1" ]]; then
    git -C "$1" checkout -q --detach "$2"
  else
    mkdir -p "$SESSION_DIR"
    git -C "$ROOT" worktree add -q --detach "$1" "$2"
  fi
}

chart_dir() {
  local chart="$1"
  [[ "$chart" == */* ]] || chart="charts/$chart"
  echo "${chart%/}"
}

# Updates file:// dependencies first (bundles before parents), each chart once per run.
build_deps() {
  local chart="$1" name version repo rest
  case "$DONE_DEPS" in *" $chart "*) return 0 ;; esac
  while read -r name version repo rest; do
    if [[ "$repo" == file://* ]]; then
      build_deps "$(cd "$chart/${repo#file://}" && pwd)"
    fi
  done < <(helm dependency list "$chart" 2>/dev/null | tail -n +2)
  echo "deps: $chart" >&2
  helm dependency build --skip-refresh "$chart" >/dev/null 2>&1 ||
    helm dependency update "$chart" >/dev/null ||
    die "dependency update failed for $chart. Run ./hack/helm-dependencies.bash once to add the Helm repositories."
  DONE_DEPS="$DONE_DEPS$chart "
}

cmd_pr() {
  local n="${1:-}" dir
  [[ "$n" =~ ^[0-9]+$ ]] || die "usage: pr <number>"
  dir="$SESSION_DIR/pr-$n"
  git -C "$ROOT" fetch -q "$REMOTE" "+pull/$n/head:refs/remotes/$REMOTE/pr/$n"
  checkout_ref "$dir" "$REMOTE/pr/$n"
  echo "PR #$n ($(git -C "$dir" rev-parse --short HEAD)) is at $dir, git ref $REMOTE/pr/$n" >&2
  echo "$dir"
}

cmd_up() {
  [[ $# -ge 2 ]] || usage 1
  local s="$1" chart src="$ROOT" release="" ns="" existing
  chart="$(chart_dir "$2")"
  shift 2
  check_name "$s"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --src) src="$(cd "$2" && pwd)"; shift 2 ;;
      --release) release="$2"; shift 2 ;;
      --namespace) ns="$2"; shift 2 ;;
      --) shift; break ;;
      *) die "unknown option '$1' (pass helm args after --)" ;;
    esac
  done
  [[ -f "$src/$chart/Chart.yaml" ]] || die "no chart at $src/$chart"
  release="${release:-$(basename "$chart")}"
  ns="${ns:-ug-$s}"
  use_cluster

  if k get namespace "$ns" >/dev/null 2>&1; then
    existing="$(k get namespace "$ns" -o jsonpath="{.metadata.labels['umbrella-guardian/session']}")"
    [[ "$existing" == "$s" ]] || die "namespace $ns exists and does not belong to session '$s'"
  else
    k create namespace "$ns" >/dev/null
    k label namespace "$ns" "$LABEL=$s" >/dev/null
  fi

  build_deps "$src/$chart"
  (cd "$src" && h upgrade --install "$release" "$chart" -n "$ns" --timeout "$TIMEOUT" "$@")
  echo "session '$s': release $release in namespace $ns from $src ($(git -C "$src" rev-parse --short HEAD 2>/dev/null || echo 'no git'))"
}

cmd_status() {
  [[ $# -eq 1 ]] || usage 1
  local ns
  use_cluster
  ns="$(session_ns "$1")"
  k wait -n "$ns" --for=condition=Ready pod --field-selector=status.phase!=Succeeded --all --timeout="${UMBRELLA_WAIT:-10m}" >/dev/null 2>&1 ||
    echo "warning: not all pods are Ready yet" >&2
  k get pods,jobs -n "$ns"
  echo
  k get ingress -n "$ns" 2>/dev/null || true
  echo
  echo "images:"
  k get pods -n "$ns" -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u
}

cmd_list() {
  use_cluster
  k get namespaces -l "$LABEL" -L "$LABEL"
  echo
  git -C "$ROOT" worktree list | grep -F "$SESSION_DIR/" || echo "no session worktrees under $SESSION_DIR"
}

render_ref() {
  local ref="$1" chart="$2" out="$3" src
  shift 3
  if [[ "$ref" == "." ]]; then
    src="$ROOT"
  else
    src="$SESSION_DIR/render-$(printf '%s' "$ref" | tr -c 'A-Za-z0-9._-' '-')"
    checkout_ref "$src" "$ref"
  fi
  [[ -f "$src/$chart/Chart.yaml" ]] || die "no chart $chart at ref $ref"
  build_deps "$src/$chart"
  (cd "$src" && helm template "$(basename "$chart")" "$chart" --namespace umbrella "$@") >"$out"
}

show_diff() {
  if cmp -s "$3" "$4"; then
    echo "no differences"
  elif command -v dyff >/dev/null 2>&1; then
    dyff between --omit-header "$3" "$4" || true
  else
    diff -u --label "$1" --label "$2" "$3" "$4" || true
  fi
}

cmd_diff_render() {
  [[ $# -ge 3 ]] || usage 1
  local a="$1" b="$2" chart out
  chart="$(chart_dir "$3")"
  shift 3
  [[ "${1:-}" == "--" ]] && shift
  out="$(mktemp -d "${TMPDIR:-/tmp}/umbrella-diff.XXXXXX")"
  render_ref "$a" "$chart" "$out/a.yaml" "$@"
  render_ref "$b" "$chart" "$out/b.yaml" "$@"
  echo "rendered: $out/a.yaml ($a) and $out/b.yaml ($b)" >&2
  show_diff "$a" "$b" "$out/a.yaml" "$out/b.yaml"
}

cmd_diff_sessions() {
  [[ $# -eq 2 ]] || usage 1
  local out s ns rel
  use_cluster
  out="$(mktemp -d "${TMPDIR:-/tmp}/umbrella-diff.XXXXXX")"
  for s in "$1" "$2"; do
    ns="$(session_ns "$s")"
    rel="$(session_release "$ns")"
    [[ -n "$rel" ]] || die "no Helm release in namespace $ns"
    h get values "$rel" -n "$ns" -o yaml >"$out/$s.values.yaml"
    h get manifest "$rel" -n "$ns" | sed "s/$ns/SESSION-NAMESPACE/g" >"$out/$s.manifest.yaml"
    k get pods -n "$ns" -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u >"$out/$s.images.txt"
  done
  echo "== user-supplied values" && show_diff "$1" "$2" "$out/$1.values.yaml" "$out/$2.values.yaml"
  echo "== images" && show_diff "$1" "$2" "$out/$1.images.txt" "$out/$2.images.txt"
  echo "== manifests (namespace normalized)" && show_diff "$1" "$2" "$out/$1.manifest.yaml" "$out/$2.manifest.yaml"
  echo "files: $out" >&2
}

cmd_down() {
  [[ $# -eq 2 && "$2" == "--yes" ]] || die "usage: down <session> --yes (deletes the session namespace)"
  local ns rel
  use_cluster
  ns="$(session_ns "$1")"
  rel="$(session_release "$ns")"
  [[ -z "$rel" ]] || h uninstall "$rel" -n "$ns" --wait --timeout "$TIMEOUT"
  k delete namespace "$ns" --wait=false
  echo "session '$1' removed (namespace $ns, PVCs included). Worktrees stay: git worktree remove <path>"
}

cmd="${1:-}"
[[ $# -gt 0 ]] && shift
case "$cmd" in
  pr) cmd_pr "$@" ;;
  up) cmd_up "$@" ;;
  status) cmd_status "$@" ;;
  list) cmd_list ;;
  diff-render) cmd_diff_render "$@" ;;
  diff-sessions) cmd_diff_sessions "$@" ;;
  down) cmd_down "$@" ;;
  -h|--help|help|"") usage 0 ;;
  *) usage 1 ;;
esac
