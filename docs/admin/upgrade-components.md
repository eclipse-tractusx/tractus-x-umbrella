# Upgrading Components

This document provides instructions for upgrading components within the Tractus-X Umbrella chart.

## Upgrading a Component to a new Version

You can upgrade a component to a new version by following these steps:

1. Update the `version` attribute in the Chart.yaml of the respective component chart, following semantic versioning principles
2. If the component is a dependency of another chart:
   - Update the dependency version in the parent chart's Chart.yaml
   - Bump the `version` attribute in the parent chart's Chart.yaml

### Example Workflow

For most components that are dependencies of the tx-data-provider:

1. Update the `version` attribute in the component's Chart.yaml
2. Update the dependency version in the Chart.yaml of [tx-data-provider](/charts/tx-data-provider)
3. Bump the `version` attribute in the Chart.yaml of [tx-data-provider](/charts/tx-data-provider)
4. Update the dependency version of `tx-data-provider` in the Chart.yaml of [umbrella](/charts/umbrella)
5. Bump the `version` attribute in the Chart.yaml of [umbrella](/charts/umbrella)

For components that are direct dependencies of the umbrella chart (like identity-and-trust-bundle):

1. Update the `version` attribute in the component's Chart.yaml
2. Update the dependency version of the component in the Chart.yaml of [umbrella](/charts/umbrella)
3. Bump the `version` attribute in the Chart.yaml of [umbrella](/charts/umbrella)

## Rollback Procedure

If issues are encountered after an upgrade:

1. Revert to the previous version in the Chart.yaml files
2. Update dependencies with `helm dependency update`
3. Redeploy using the previous version
