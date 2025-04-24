#!/bin/bash

# Check if any repositories is present
if ! helm repo list ; then
  echo "Need to add repos"
  helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev
  helm repo add hashicorp https://helm.releases.hashicorp.com
  helm repo add runix https://helm.runix.net
fi

CHARTS_DIR="./charts"

echo "🔄 Updating Helm repositories..."
helm repo update

echo "🔍 Scanning for Helm charts under '$CHARTS_DIR'..."
# find all Chart.yaml files, dedupe their parent dirs, and update each
find "$CHARTS_DIR" -type f -name Chart.yaml -print0 \
  | while IFS= read -r -d '' chartfile; do
      chartdir=$(dirname "$chartfile")
      echo -e "\n📦 Updating dependencies for chart: $chartdir"
      helm dependency update "$chartdir"
    done

echo -e "\n✅ All charts up to date!"
