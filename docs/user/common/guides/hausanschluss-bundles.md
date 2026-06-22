## Introduction

The **"Hausanschluss" Bundles** are a set of helm charts that simplify deployment of all the Tractus-X enablement
services into modular, independently deployable Capability Bundles. Its goal is to reduce deployment complexity, enable
“bring-your-own” components, and accelerate onboarding for product developers, testers, and SMEs.

This document mainly refers to usage of the "Hausanschluss" Bundles without the Umbrella Chart.
To install the bundles as part of the Umbrella Chart, please refer to the [README.md](/README.md#usage).

### Prerequisites & Skills

For general prerequisites and system requirements, please refer to:
- [Main Prerequisites](/README.md#prerequisites)

For complete installation instructions, follow the Umbrella setup guides:

1. [Cluster Setup](/docs/README.md#setup-network--installation)
2. [Network Setup](/docs/README.md#setup-network--installation)
3. [Installation](/docs/README.md#setup-network--installation)

Additional requirements specific to the usage of Hausanschluss Bundles without the umbrella chart:

- **Access & Credentials**
   - Kubernetes RBAC role permitting chart installation in target namespace.
  - (Optional) Vault token or AppRole credentials, if not using Vault subchart.

- **Required Skills**
   - Familiarity with Vault's secret engines and Kubernetes authentication.

### Bundle Overview

The umbrella chart is organized into four main Capability Bundles (each a Helm subchart):

| Bundle                 | Default Components                                      | Remappable via BYO                        |
|------------------------|---------------------------------------------------------|-------------------------------------------|
| Identity & Trust       | ssi-dim-wallet-stub                                     | Replaceable with your own Identity Wallet |
| Dataspace Connector    | Eclipse Dataspace Connector, PostgreSQL, Vault subchart | Vault / PostgreSQL can be swapped out     |
| Digital Twin           | Digital Twin Registry (DTR), PostgreSQL                 | PostgreSQL can be swapped out             |
| Data Persistence Layer | Simple Submodel Server                                  | -                                         |

You can enable or disable any bundle independently and supply your own implementations.

## Installation Guide

### Add the Helm Repository

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm repo update
```

### Update the Chart Dependencies

```bash
helm dependency update charts/data-persistence-layer-bundle
helm dependency update charts/dataspace-connector-bundle
helm dependency update charts/digital-twin-bundle
helm dependency update charts/identity-and-trust-bundle
```

### Deploying the Charts

#### Umbrella

To install the entire umbrella Chart, see [README.md](/README.md).

#### Install a single Bundle

Install a bundle with its default values:

##### Dataspace Connector Bundle

```bash
helm install connector tractusx-dev/dataspace-connector-bundle \
  --namespace umbrella --create-namespace
```

##### Data Persistence Layer Bundle

```bash
helm install submodel-server tractusx-dev/data-persistence-layer-bundle \
  --namespace umbrella --create-namespace
```

##### Digital Twin Bundle

> ⚠️ Due to an issue in the sldt-digital-twin-registry Helm Chart, the dataSource.url cannot be templated and has to be set manually to the release name

```bash
helm install dtr tractusx-dev/digital-twin-bundle \
  --namespace umbrella --create-namespace \
  --set digital-twin-registry.registry.dataSource.url=jdbc:postgresql://dtr-postgresql:5432/dtr
```

##### Identity and Trust Bundle

```bash
helm install wallet tractusx-dev/identity-and-trust-bundle \
  --namespace umbrella --create-namespace
```

#### Use a bundle as dependencies

Create your own Chart and add the bundles as dependency.

```yaml
dependencies:
  - name: dataspace-connector-bundle
    version: 1.0.0
    repository: https://eclipse-tractusx.github.io/charts/dev
```

The Bundles are pre-configured to work with in the Umbrella environment.  
In case you want to use them in your own dataspace, you have to adjust the "Decentralized Claims Protocol (DCP, formerly IATP) Settings"
of the dataspace-connector-bundle with credentials of your own dataspace.

```yaml
dataspace-connector-bundle:
  tractusx-connector:
    iatp:
      id: <your-did>
      trustedIssuers:
        - <the-trusted-issuer-did>
      sts:
        dim:
          url: <your-wallet-dim-url>
        oauth:
          token_url: <your-wallet-token-url>
          client:
            id: <your-client-id>
            secret_alias: edc-wallet-secret-vault-alias
```

## Customizing Your Deployment

### Bring-Your-Own Components

Each Capability Bundle supports Bring-Your-Own (BYO) of its dependencies:

1. Disable the built-in subchart (e.g. `postgresql.enabled=false`).

2. Configure the external service.  
   They are marked with `# === Bring Your Own ===` in the values.yaml files or with `(Bring your Own)` in the README files
   of each Bundle Chart.

3. Ensure connectivity (NetworkPolicy, ServiceAccounts, Secrets).

#### Example: Bring your own Vault

Create your Chart with the dataspace-connector-bundle as a dependency:

```yaml
dependencies:
  - name: dataspace-connector-bundle
    version: 1.0.0
    repository: https://eclipse-tractusx.github.io/charts/dev
```

Configure the dataspace-connector-bundle to use your own vault.

```yaml
dataspace-connector-bundle:
  tractusx-connector:
    # === Bring Your Own ===
    vault:
      hashicorp:
        url: "<your-own-vault>"
        token: "<your-vault-token>"
        paths:
          secret: <your-base-path-to-secrets>
          folder: "<your-sub-folder>" # Optional if the secrets are on root level
  vault:
    enabled: false # To save resources, make sure to disable the embedded vault.
```

### Configuration options

See the chart README for detailed configuration options:

- [data-persistence-layer-bundle](/charts/data-persistence-layer-bundle/README.md)
- [dataspace-connector-bundle](/charts/dataspace-connector-bundle/README.md)
- [digital-twin-bundle](/charts/digital-twin-bundle/README.md)
- [identity-and-trust-bundle](/charts/identity-and-trust-bundle/README.md)

## Updating & Uninstalling

### To update a chart

```bash
helm repo update
helm upgrade connector tractusx-dev/dataspace-connector-bundle \
  --namespace umbrella \
  -f values.custom.yaml
```

### To uninstall

```bash
helm uninstall connector --namespace umbrella
kubectl delete ns umbrella
```

### To upgrade components
For information on upgrading components to a new version, please refer to the [Upgrading Components](/docs/admin/upgrade-components.md) guide.

## Troubleshooting

| Symptom | Possible Cause | Remedy |
|---------|----------------|--------|

Use `kubectl describe pod <pod>` and `kubectl logs <pod>` to inspect errors in detail.

## FAQ

1. Can I deploy multiple instances of the same bundle?  
   Yes. Choose a unique release name and deploy multiple instances like this:
    ```bash
    helm install edc-a charts/dataspace-connector-bundle -n umbrella --create-namespace \
    --set tractusx-connector.controlplane.ingresses[0].hostname=edc-a.controlplane.tx.test \
    --set tractusx-connector.dataplane.ingresses[0].hostname=edc-a.dataplane.tx.test

    helm install edc-b charts/dataspace-connector-bundle -n umbrella --create-namespace \
    --set tractusx-connector.controlplane.ingresses[0].hostname=edc-b.controlplane.tx.test \
    --set tractusx-connector.dataplane.ingresses[0].hostname=edc-b.dataplane.tx.test
    ```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
