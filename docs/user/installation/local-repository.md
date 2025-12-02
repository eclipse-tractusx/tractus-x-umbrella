# Install from local repository

## Table of Contents

- [Prerequisites](#prerequisites)
- [First Steps](#first-steps)
- [Custom Configuration](#custom-configuration)
- [Data Exchange Subset](#data-exchange-subset)
  - [Enable Additional Data Consumers](#enable-additional-data-consumers)
- [Portal Subset](#portal-subset)

## Prerequisites

Before proceeding, ensure you have:
- A running Kubernetes cluster (see [Cluster Setup](../setup/README.md)).
- `helm` and `kubectl` installed.
- Cloned the [tractus-x-umbrella](https://github.com/eclipse-tractusx/tractus-x-umbrella) repository.

## First Steps

1. **Update Dependencies**: Update the chart dependencies of the umbrella helm chart.
   ```bash
   bash hack/helm-dependencies.bash 
   ```

2. **Navigate to Chart**: Move to the chart directory.
   ```bash
   cd charts/umbrella/
   ```

## Custom Configuration

If you have a custom configuration file (e.g., `your-values.yaml`), use the following command:

```bash
helm install -f your-values.yaml umbrella . --namespace umbrella --create-namespace
```

> [!NOTE]
> **Command Explanation**
> 
> The installation commands generally follow this structure:
> `helm install -f <VALUES_FILE> <RELEASE_NAME> . --namespace <NAMESPACE> --create-namespace`
> 
> - `-f <VALUES_FILE>`: Specifies the configuration file (e.g., `values-adopter-portal.yaml`).
> - `<RELEASE_NAME>`: Name of the release (e.g., `umbrella`).
> - `.`: Path to the chart (current directory).
> - `--namespace <NAMESPACE>`: Target namespace.
> - `--create-namespace`: Creates the namespace if it doesn't exist.

> [!TIP]
> For production or specific setups, it is highly recommended to use your own values file to manage configurations and secrets.

## Data Exchange Subset

This subset is designed for the **E2E Adopter Journey** and enables secure data sharing.

```bash
helm install -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella --create-namespace
```

### Enable Additional Data Consumers

To enable a second data consumer (`dataconsumerTwo`):

1. **Edit Configuration**: Open `values-adopter-data-exchange.yaml` and set `enabled: true`.
   ```yaml
   dataconsumerTwo:
     enabled: true
   ```

2. **Apply Changes**: Upgrade the Helm release.
   ```bash
   helm upgrade -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella
   ```

## Portal Subset

This subset provides the user interface for onboarding and management.

```bash
helm install -f values-adopter-portal.yaml umbrella . --namespace umbrella --create-namespace
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
