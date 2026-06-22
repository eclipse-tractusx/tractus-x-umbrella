# Install from released chart

Add the Eclipse Tractus-X [charts repository](https://github.com/eclipse-tractusx/charts):

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
```

**:grey_question: Command explanation**:

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

## Install with your chosen components enabled

```bash
helm install \
  --set COMPONENT_1.enabled=true,COMPONENT_2.enabled=true,COMPONENT_3.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

## Data Exchange Subset

This subset supports secure data sharing between participants (currently in focus of the **E2E Adopter Journey**).

### Installation Command

```bash
helm install \
  --set identity-and-trust-bundle.enabled=true,dataconsumerOne.enabled=true,tx-data-provider.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

### Optional: Enable Additional Data Consumers

To enable a second data consumer `dataconsumerTwo`, use the following upgrade command:

```bash
helm upgrade \
  --set dataconsumerTwo.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella
```

## Portal Subset

This subset provides a web interface for participant onboarding and management.

### Installation Command

```bash
helm install \
  --set portal.enabled=true,centralidp.enabled=true,sharedidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

## BPDM Subset

The BPDM (Business Partner Data Management) subset manages business partner master data.

### Installation Command

```bash
helm install \
  --set bpdm.enabled=true,centralidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

## Custom Configuration

You can customize the installation by providing your own `values.yaml` file. For example:

```bash
helm install -f your-values.yaml umbrella tractusx-dev/umbrella --namespace umbrella --create-namespace
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
