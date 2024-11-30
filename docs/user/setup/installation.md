
# Installation

This guide provides instructions to install the Umbrella Chart and its predefined subsets.

> **Note**
> There are two basic option to locally deploy the Umbrella chart:
> - Using already released charts from the Helm repository
> - Using the local charts from the repository

The currently available components are following:

- [portal](https://github.com/eclipse-tractusx/portal/tree/portal-2.0.0)
- [centralidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.0.0-alpha.2)
- [sharedidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.0.0-alpha.1)
- [bpndiscovery](https://github.com/eclipse-tractusx/sldt-bpn-discovery/tree/bpndiscovery-0.2.2)
- [discoveryfinder](https://github.com/eclipse-tractusx/sldt-discovery-finder/tree/discoveryfinder-0.2.2)
- [sdfactory](https://github.com/eclipse-tractusx/sd-factory/tree/sdfactory-2.1.21)
- [managed-identity-wallet](https://github.com/eclipse-tractusx/managed-identity-wallet/tree/v0.4.0)
- [semantic-hub](https://github.com/eclipse-tractusx/sldt-semantic-hub/tree/semantic-hub-0.2.2)
- [ssi credential issuer](https://github.com/eclipse-tractusx/ssi-credential-issuer/tree/v1.0.0)
- [dataconsumerOne](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.7.1), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0))
- [tx-data-provider](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.7.1), [digital-twin-registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/digital-twin-registry-0.4.5), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0), [simple-data-backend](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/simple-data-backend))
- [dataconsumerTwo](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.7.1), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0))
- [bdrs](https://github.com/eclipse-tractusx/bpn-did-resolution-service/tree/0.5.2) (**in memory** - no persistance possible)
- [iatp-mock](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/umbrella/charts/iatpmock/Chart.yaml)
- [bpdm](https://github.com/eclipse-tractusx/bpdm/tree/release/6.0.x)
- [ssi-dim-wallet-stub](https://github.com/eclipse-tractusx/ssi-dim-wallet-stub/releases/tag/ssi-dim-wallet-stub-0.1.2)

> :warning: **Note**
>
> Please be aware of [Note for R24.05](#note-for-r2405)
>
> - Due to resource restrictions, it's **not recommended** to install the helm chart with all components enabled.
>
> - It is to be expected that some pods - which run as post-install hooks, like for instance the **portal-migrations job - will run into errors until another component**, like for instance a database, is ready to take connections.
    > Those jobs will recreate pods until one run is successful.
>
> - **Persistance is disabled by default** but can be configured in a custom values file.

## Predefined Subsets (released charts)

The Umbrella Chart supports predefined subsets designed for specific use cases. Choose the subset based on your requirements.

### Install with your chosen components enabled

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
```

**:grey_question: Command explanation**

> `helm install` is used to install a chart in Kubernetes using Helm.
> > `--set COMPONENT_1.enabled=true,COMPONENT_2.enabled=true` Enables the components by setting their respective enabled values to true.
>
> > `umbrella` is the release name for the chart.
>
> > `tractusx-dev/umbrella` specifies the chart to install, with *tractusx-dev* being the repository name and *umbrella* being the chart
name.
>
> > `--namespace umbrella` specifies the namespace in which to install the chart.
>
> > `--create-namespace` create a namespace with the name `umbrella`.

```bash
helm install \
  --set COMPONENT_1.enabled=true,COMPONENT_2.enabled=true,COMPONENT_3.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

### Data Exchange Subset

This subset supports secure data sharing between participants (currently in focus of the **E2E Adopter Journey**).

#### Installation Command

```bash
helm install \
  --set centralidp.enabled=true,managed-identity-wallet.enabled=true,dataconsumerOne.enabled=true,tx-data-provider.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

#### Optional: Enable Additional Data Consumers

To enable a second data consumer `dataconsumerTwo`, use the following upgrade command:

```bash
helm upgrade \
  --set dataconsumerTwo.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella
```

### Portal Subset

This subset provides a web interface for participant onboarding and management.

#### Installation Command

```bash
helm install \
  --set portal.enabled=true,centralidp.enabled=true,sharedidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

### BPDM Subset

The BPDM (Business Partner Data Management) subset manages business partner master data.

#### Installation Command

```bash
helm install \
  --set bpdm.enabled=true,centralidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

### Custom Configuration

You can customize the installation by providing your own `values.yaml` file. For example:

```bash
helm install -f your-values.yaml umbrella tractusx-dev/umbrella --namespace umbrella --create-namespace
```

## Predefined Subsets (local repository)

Make sure to clone the [tractus-x-umbrella](https://github.com/eclipse-tractusx/tractus-x-umbrella) repository beforehand and navigate to the `charts/umbrella` directory.
```bash
cd charts/umbrella/
```

Download the dependencies of the tx-data-provder subchart:
```bash
helm dependency update ../tx-data-provider
```

Download the chart dependencies of the umbrella helm chart:
```bash
helm dependency update
```

**:grey_question: Command explanation**

> `helm install` is used to install a Helm chart.
> > `-f your-values.yaml` | `-f values-*.yaml` specifies the values file to use for configuration.
>
> > `umbrella` is the release name for the Helm chart.
>
> > `.` specifies the path to the chart directory.
>
> > `--namespace umbrella` specifies the namespace in which to install the chart.
>
> > `--create-namespace` create a namespace with the name `umbrella`.

### Custom Configuration

Install your chosen components by having them enabled in a `your-values.yaml` file:

```bash
helm install -f your-values.yaml umbrella . --namespace umbrella --create-namespace
```

> In general, all your specific configuration and secret values should be set by installing with an own values file.

Choose to install one of the predefined subsets (currently in focus of the **E2E Adopter Journey**):

### Data Exchange Subset

The Data Exchange subset enables secure data sharing between participants in the network.

```bash
helm install -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella --create-namespace
```

#### Enable Additional Data Consumers

To enable an additional data consumer (`dataconsumerTwo`), follow these steps:

1. Update the `values-adopter-data-exchange.yaml` file to set `dataconsumerTwo` as enabled:
   ```yaml
   dataconsumerTwo:
     enabled: true
   ```

2. Apply the changes by upgrading the Helm release:
   ```bash
   helm upgrade -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella
   ```

#### Using the IATP-Mock Version

To use the IATP-Mock version of the Data Exchange subset, run:
```bash
helm install -f values-adopter-data-exchange-iatp-mock.yaml umbrella . --namespace umbrella --create-namespace
```

### Portal Subset

The Portal subset provides a user-friendly interface for participant onboarding and management.

```bash
helm install -f values-adopter-portal.yaml umbrella . --namespace umbrella --create-namespace
```

## Notes

- Ensure your Kubernetes cluster meets the minimum system requirements.
- Some pods may take time to initialize as they wait for dependencies to become ready.
- Persistence is disabled by default but can be enabled through custom values.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
