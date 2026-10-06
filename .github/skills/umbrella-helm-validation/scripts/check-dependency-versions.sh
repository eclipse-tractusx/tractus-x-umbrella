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

# Fails if any file:// dependency version differs from the referenced chart's version.
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

fail=0
for chart in charts/*/; do
  chart="${chart%/}"
  [[ -f "$chart/Chart.yaml" ]] || continue
  while read -r name version repo _; do
    [[ "$repo" == file://* ]] || continue
    dep_path="$chart/${repo#file://}"
    actual="$(helm show chart "$dep_path" | awk '/^version:/ {print $2; exit}')"
    if [[ "$version" == "$actual" ]]; then
      echo "OK        $chart -> $name $version"
    else
      echo "MISMATCH  $chart -> $name requires $version but $dep_path is $actual"
      fail=1
    fi
  done < <(helm dependency list "$chart" 2>/dev/null | tail -n +2)
done

exit "$fail"
