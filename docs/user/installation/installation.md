# Installation

This guide provides instructions to install the Umbrella Chart and its predefined subsets.

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
> Please be aware of [Note for R24.05](../note-r2405-onwards)
>
> - Due to resource restrictions, it's **not recommended** to install the helm chart with all components enabled.
>
> - It is to be expected that some pods - which run as post-install hooks, like for instance the **portal-migrations job - will run into errors until another component**, like for instance a database, is ready to take connections.
    > Those jobs will recreate pods until one run is successful.
>
> - **Persistance is disabled by default** but can be configured in a custom values file.

## Possible ways for installation

- Using [already released](released-charts.md) charts from the Helm repository
- Using the [local charts](local-charts.md) from the repository

## Notes

- Ensure your Kubernetes cluster meets the minimum system requirements.
- Some pods may take time to initialize as they wait for dependencies to become ready.
- Persistence is disabled by default but can be enabled through custom values.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>