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

See the [umbrella chart structure](/docs/user/linux/installation/README.md#available-components) to understand how the "Hausanschluss" Bundles, `tx-data-provider` and other charts depend on each other.

## Rollback Procedure

If issues are encountered after an upgrade:

1. Revert to the previous version in the Chart.yaml files
2. Update dependencies with `helm dependency update`
3. Redeploy using the previous version

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
