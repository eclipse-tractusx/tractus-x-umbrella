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

#### Skills:

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

### Deploying the Charts

#### Umbrella

To install the entire umbrella Chart, see [README.md](README.md).

#### Choose your Bundles

Dependent on your needs, you can choose which bundles to install. To do that, choose one of two recommended options:

1. Install only the Chart

Install the bundles:

```
helm install data-persistence tractusx-dev/data-persistence-layer-bundle \
  --namespace umbrella --create-namespace
```

This will install the chart with the default values.

Use the charts as dependencies:

```yaml
dependencies:
  - name: identity-and-trust-bundle
    version: 1.0.1
    repository: https://eclipse-tractusx.github.io/charts/dev

  - name: dataspace-connector-bundle
    version: 1.0.1
    repository: https://eclipse-tractusx.github.io/charts/dev
```

The Bundles are pre-configured to work with in the Umbrella environment. 
In case you want to use them in your own 

and set the values to your need:

```yaml
identity-and-trust-bundle:
  wallet:
    host: ssi-dim-wallet-stub.tx.test

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

### Customizing Your Deployment

## Bring-Your-Own Components

Each Capability Bundle supports BYO of its dependencies:

1. Disable the built-in subchart (e.g. `postgresql.enabled=false`).

2. Configure the external service.  
They are marked with `# === Bring Your Own ===` in the values.yaml files or with (Bring your Own) in the README files of each Bundle Chart.

3. Ensure connectivity (NetworkPolicy, ServiceAccounts, Secrets).

## Updating & Uninstalling

### To update a chart

```bash
helm repo update
helm upgrade data-persistence tractusx-dev/data-persistence-layer-bundle \
  --namespace umbrella \
  -f values.custom.yaml
```

### To uninstall

```bash
helm uninstall data-persistence --namespace umbrella
kubectl delete ns umbrella
```

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
