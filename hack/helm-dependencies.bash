#!/bin/bash

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
fi

CHARTS_DIR="./charts"
TX_DATA_PROVIDER_DIR="$CHARTS_DIR/tx-data-provider"
UMBRELLA_DIR="$CHARTS_DIR/umbrella"

echo "🔄 Updating Helm repositories..."
helm repo update

echo "🔍 Updating dependencies for Helm charts under '$CHARTS_DIR'..."

# Update dependencies for all charts except tx-data-provider and umbrella
for chartdir in "$CHARTS_DIR"/*; do
  if [[ -d "$chartdir" && -f "$chartdir/Chart.yaml" && "$chartdir" != "$TX_DATA_PROVIDER_DIR" && "$chartdir" != "$UMBRELLA_DIR" ]]; then
    echo -e "\n📦 Updating dependencies for chart: $chartdir"
    helm dependency update "$chartdir" --skip-refresh
  fi
done

# Update tx-data-provider and umbrella at the end
echo -e "\n📦 Updating dependencies for chart: $TX_DATA_PROVIDER_DIR"
helm dependency update "$TX_DATA_PROVIDER_DIR" --skip-refresh

echo -e "\n📦 Updating dependencies for chart: $UMBRELLA_DIR"
helm dependency update "$UMBRELLA_DIR" --skip-refresh

echo -e "\n✅ All charts up to date!"
