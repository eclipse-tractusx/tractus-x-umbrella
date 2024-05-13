#!/bin/bash

# Check if any repositories is present
if ! helm repo list ; then
  echo "Need to add repos"
  helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev
  helm repo add hashicorp https://helm.releases.hashicorp.com
  helm repo add runix https://helm.runix.net
fi

# This hack script will download all chart/umbrella dependency charts.
# (including recursive dependencies)
find charts/umbrella -name Chart.yaml -print | \
  sed s/Chart.yaml//g | \
  awk -F"/" '{print NF $0}' | \
  sort -nr | \
  sed 's/^.//' | \
  xargs -n1 helm dependency update --skip-refresh
