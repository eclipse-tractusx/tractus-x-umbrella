# Installation

This guide provides instructions to install the Umbrella Chart and its predefined subsets.

## Available components

The currently available components are the following:

- [portal](https://github.com/eclipse-tractusx/portal/tree/portal-2.5.0)
- [centralidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.2.0)
- [sharedidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.2.0)
- [bpndiscovery](https://github.com/eclipse-tractusx/sldt-bpn-discovery/tree/bpndiscovery-0.5.1)
- [discoveryfinder](https://github.com/eclipse-tractusx/sldt-discovery-finder/tree/discoveryfinder-0.5.1)
- [sdfactory](https://github.com/eclipse-tractusx/sd-factory/tree/sdfactory-2.1.24)
- [semantic-hub](https://github.com/eclipse-tractusx/sldt-semantic-hub/tree/semantic-hub-0.5.0)
- [ssi credential issuer](https://github.com/eclipse-tractusx/ssi-credential-issuer/tree/v1.4.0)
- [tx-data-provider](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider)
  - [dataspace-connector-bundle](../../../charts/dataspace-connector-bundle)
    - [tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.10.0)
    - [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0)
  - [digital-twin-bundle](../../../charts/digital-twin-bundle)
    - [digital-twin-registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/digital-twin-registry-0.7.0)
  - [data-persistence-layer-bundle](../../../charts/data-persistence-layer-bundle)
    - [simple-data-backend](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/simple-data-backend-0.1.0)
- [dataconsumerOne](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider)
  - [dataspace-connector-bundle](../../../charts/dataspace-connector-bundle)
    - [tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.10.0)
    - [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0)
- [dataconsumerTwo](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider)
  - [dataspace-connector-bundle](../../../charts/dataspace-connector-bundle)
    - [tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.10.0)
    - [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0)
- [bdrs](https://github.com/eclipse-tractusx/bpn-did-resolution-service/tree/0.5.2) (**in memory** - no persistence possible)
- [bpdm](https://github.com/eclipse-tractusx/bpdm/tree/release/7.0.x)
- [identity-and-trust-bundle](../../../charts/identity-and-trust-bundle)
  - [ssi-dim-wallet-stub](https://github.com/eclipse-tractusx/ssi-dim-wallet-stub/releases/tag/ssi-dim-wallet-stub-0.1.8)

## Auxiliary components

The currently available auxiliary components are following:

- [pgadmin4](https://artifacthub.io/packages/helm/runix/pgadmin4/1.25.0)
- [opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/opentelemetry-collector-0.90.0)
- [jaeger](https://github.com/jaegertracing/helm-charts/tree/jaeger-3.0.7)
- [prometheus](https://github.com/prometheus-community/helm-charts/tree/prometheus-27.1.08)
- [grafana](https://github.com/grafana/helm-charts/tree/grafana-8.10.1)
- [loki](https://github.com/grafana/loki/tree/helm-loki-6.27.0)

> :warning: **Note**
>
> Please be aware of [Note for R24.05](/docs/user/note-r2405-onwards)
>
> - Due to resource restrictions, it's **not recommended** to install the helm chart with all components enabled.
>
> - It is to be expected that some pods - which run as post-install hooks, like for instance the **portal-migrations job - will run into errors until another component**, like for instance a database, is ready to take connections.
    > Those jobs will recreate pods until one run is successful.
>
> - **Persistence is disabled by default** but can be configured in a custom values file.

## Possible ways for installation

- Checking out this umbrella repository and using the [helm chart locally](local-repository.md)
- Using [released helm chart](released-chart.md)

## Notes

- Ensure your Kubernetes cluster meets the minimum system requirements.
- Some pods may take time to initialize as they wait for dependencies to become ready.
- Persistence is disabled by default but can be enabled through custom values.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
