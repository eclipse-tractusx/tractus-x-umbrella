## Introduction

The **“Hausanschluss” Bundle** is a set of Helm Charts that simplifies deployment of all the Catena-X enablement
services into modular, independently deployable Capability Bundles. Its goal is to reduce deployment complexity, enable
“bring-your-own” components, and accelerate onboarding for product developers, testers, and SMEs.

### Prerequisites & Skills

Before you begin, make sure you have the following:

- **Kubernetes cluster** (v1.24+; any conformant distribution: EKS, AKS, GKE, on-premise, Kind/Minikube).
- **Helm CLI** (v3.8+).
- **kubectl** (matching your cluster version).
- (Optional) **Vault CLI** (for secret provisioning; if you use HashiCorp Vault).
- (Optional) **Docker client** (only if building or pushing custom images).
- **Access & Credentials**
    - Kubernetes RBAC role permitting chart installation in target namespace.
    - (Optional) Vault token or AppRole credentials, if using Vault subchart.
    - (Optional) Docker registry credentials, if you override images.
- Umbrella setup guides
    1. [Cluster Setup](/docs/user/setup)
    2. [Network Setup](/docs/user/network)
    3. [Installation](/docs/user/installation)

#### Skills

- Comfortable editing `values.yaml` and using Helm’s `--set` flags.
- Familiarity with Vault’s secret engines and Kubernetes authentication.
- Basic understanding of microservice architecture and Kubernetes objects (Deployments, Services, Secrets, ConfigMaps).

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

##### dataspace-connector-bundle

```bash
helm install connector tractusx-dev/dataspace-connector-bundle \
  --namespace umbrella --create-namespace
```

##### data-persistence-layer-bundle

```bash
helm install submodel-server tractusx-dev/data-persistence-layer-bundle \
  --namespace umbrella --create-namespace
```

##### digital-twin-bundle

> ⚠️ Due to an issue in the sldt-digital-twin-registry Helm Chart, the dataSource.url cannot be templated and has to be set manually to the release name

```bash
helm install dtr tractusx-dev/digital-twin-bundle \
  --namespace umbrella --create-namespace \
  --set digital-twin-registry.registry.dataSource.url=jdbc:postgresql://dtr-postgresql:5432/dtr
```

##### identity-and-trust-bundle

```bash
helm install wallet tractusx-dev/identity-and-trust-bundle \
  --namespace umbrella --create-namespace
```

#### Use a bundle as dependencies

Create your own Chart and add the bundles as dependency.

```yaml
dependencies:
  - name: dataspace-connector-bundle
    version: 1.0.1
    repository: https://eclipse-tractusx.github.io/charts/dev
```

The Bundles are pre-configured to work with in the Umbrella environment.  
In case you want to use them in your own dataspace, you have to adjust the "Identity and Trust Protocol (IATP) Settings"
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

Each Capability Bundle supports BYO of its dependencies:

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
    version: 1.0.1
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

## Releasing a new Bundle Version

You can release a new version of the Bundles by following these steps:
- update the `version` attribute in the Chart.yaml of the respective Chart 
- update the dependency version in the Chart.yaml of [tx-data-provider](/charts/tx-data-provider)
- bump the `version` attribute in the Chart.yaml of [tx-data-provider](/charts/tx-data-provider)
- update the dependency version in the Chart.yaml of [umbrella](/charts/umbrella)
- bump the `version` attribute in the Chart.yaml of [umbrella](/charts/umbrella)

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
