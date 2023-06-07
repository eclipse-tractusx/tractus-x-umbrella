#!/bin/bash

# This hack script will download all chart/umbrella dependency charts.
# (including recursive dependencies)

find charts/umbrella -name Chart.yaml -print | \
  sed s/Chart.yaml//g | \
  awk -F"/" '{print NF $0}' | \
  sort -nr | \
  sed 's/^.//' | \
  xargs -n1 helm dependency update --skip-refresh
