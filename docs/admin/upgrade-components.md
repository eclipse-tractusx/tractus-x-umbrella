# Upgrading Components

This document provides instructions for upgrading components within the Tractus-X Umbrella chart.

## Upgrading a Component to a new Version

You can upgrade a component to a new version by following these steps:

### For Components that are Direct Dependencies of the Umbrella Chart

1. **Update the Dependency Version**: In the `Chart.yaml` of the [umbrella chart](/charts/umbrella), update the dependency version for the respective component, following the chart version mentioned in the [Tractus-X releases](https://github.com/eclipse-tractusx/tractus-x-release/releases).
2. **Check Configuration in `values.yaml`**: Determine if the configuration in the `values.yaml` file of the umbrella chart needs to be updated:
   - Compare the `values.yaml` file of the respective component by diffing the currently used version with the version you want to upgrade to.
   - Make any necessary changes to the `values.yaml` file of the umbrella chart.
3. **Update the Version Attribute**: Update the version attribute in the `Chart.yaml` of the umbrella chart, following semantic versioning principles.

### For Components that are Dependencies of the `tx-data-provider` or of the "Hausanschluss" Bundles (Indirect Dependencies of the umbrella)

1. **Update the Dependency Version**: In the `Chart.yaml` of the `tx-data-provider` or bundle, update the dependency version for the respective component, following the chart version mentioned in the [Tractus-X releases](https://github.com/eclipse-tractusx/tractus-x-release/releases).
2. **Check Configuration in `values.yaml`**: Determine if the configuration in the `values.yaml` file of the umbrella chart needs to be updated:
   - Compare the `values.yaml` file of the respective component by diffing the currently used version with the version you want to upgrade to.
   - Make any necessary changes to the `values.yaml` file of the umbrella chart.
3. **Update the Version Attribute**: Update the version attribute in the `Chart.yaml` of the `tx-data-provider` or bundle, following semantic versioning principles.
4. Update the dependency version of `tx-data-provider` and the version attribute in the `Chart.yaml` of the umbrella chart.
5. If the bundle is used as a dependency of the umbrella chart (e.g., `identity-and-trust-bundle`), update the dependency version of the bundle and the version attribute in the `Chart.yaml` of the umbrella chart.

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
