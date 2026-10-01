#!/bin/bash
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

set -euo pipefail

# Check if any repositories is present
if ! helm repo list ; then
  echo "Need to add repos"
  helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev
  helm repo add hashicorp https://helm.releases.hashicorp.com
  helm repo add runix https://helm.runix.net
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
  helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo add grafana https://grafana.github.io/helm-charts
  helm repo add cert-manager https://charts.jetstack.io
else
  echo "Checking and adding missing repositories..."
  
  # Check for each required repository and add if missing
  if ! helm repo list | grep -q "^tractusx[[:space:]]"; then
    echo "Adding tractusx repository..."
    helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev
  fi

  if ! helm repo list | grep -q "^hashicorp[[:space:]]"; then
    echo "Adding hashicorp repository..."
    helm repo add hashicorp https://helm.releases.hashicorp.com
  fi

  if ! helm repo list | grep -q "^runix[[:space:]]"; then
    echo "Adding runix repository..."
    helm repo add runix https://helm.runix.net
  fi

  if ! helm repo list | grep -q "^bitnami[[:space:]]"; then
    echo "Adding bitnami repository..."
    helm repo add bitnami https://charts.bitnami.com/bitnami
  fi
  
  if ! helm repo list | grep -q "^open-telemetry[[:space:]]"; then
    echo "Adding open-telemetry repository..."
    helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
  fi
  
  if ! helm repo list | grep -q "^jaegertracing[[:space:]]"; then
    echo "Adding jaegertracing repository..."
    helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
  fi
  
  if ! helm repo list | grep -q "^prometheus-community[[:space:]]"; then
    echo "Adding prometheus-community repository..."
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  fi
  
  if ! helm repo list | grep -q "^grafana[[:space:]]"; then
    echo "Adding grafana repository..."
    helm repo add grafana https://grafana.github.io/helm-charts
  fi
  
  if ! helm repo list | grep -q "^cert-manager[[:space:]]"; then
    echo "Adding cert-manager repository..."
    helm repo add cert-manager https://charts.jetstack.io
  fi
fi

# Register additional repositories before using --skip-refresh below.
for repo_spec in \
  "basyx https://eclipse-basyx.github.io/charts" \
  "external-secrets https://charts.external-secrets.io"; do
  read -r repo_name repo_url <<< "$repo_spec"
  if ! helm repo list | grep -q "^${repo_name}[[:space:]]"; then
    helm repo add "$repo_name" "$repo_url"
  fi
done

CHARTS_DIR="./charts"
TX_DATA_PROVIDER_DIR="$CHARTS_DIR/tx-data-provider"
DECENTRALIZED_CONNECTOR_DIR="$CHARTS_DIR/decentralized-identity-connector"
UMBRELLA_DIR="$CHARTS_DIR/umbrella"

echo "🔄 Updating Helm repositories..."
helm repo update

echo "🔍 Updating dependencies for Helm charts under '$CHARTS_DIR'..."

# Resolve leaf bundles before their provider and decentralized connector parents.
for chartdir in "$CHARTS_DIR"/*; do
  if [[ -d "$chartdir" && -f "$chartdir/Chart.yaml" && "$chartdir" != "$TX_DATA_PROVIDER_DIR" && "$chartdir" != "$DECENTRALIZED_CONNECTOR_DIR" && "$chartdir" != "$UMBRELLA_DIR" ]]; then
    echo -e "\n📦 Updating dependencies for chart: $chartdir"
    helm dependency update "$chartdir" --skip-refresh
  fi
done

# Update tx-data-provider and umbrella at the end
echo -e "\n📦 Updating dependencies for chart: $TX_DATA_PROVIDER_DIR"
helm dependency update "$TX_DATA_PROVIDER_DIR" --skip-refresh

echo -e "\n📦 Updating dependencies for chart: $DECENTRALIZED_CONNECTOR_DIR"
helm dependency update "$DECENTRALIZED_CONNECTOR_DIR" --skip-refresh

echo -e "\n📦 Updating dependencies for chart: $UMBRELLA_DIR"
helm dependency update "$UMBRELLA_DIR" --skip-refresh

echo -e "\n✅ All charts up to date!"
