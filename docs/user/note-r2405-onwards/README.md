# Note from R24.05 onwards

:warning: The 24.05 Release does not include a Managed Identity Wallet (MIW) - aka the FOSS Wallet of Eclipse Tractus-X - as it was not - yet - able to cover functionalities required for the Self-Sovereign Identity Flow introduced with R24.05. To test and ship R24.05, a commercial solution was used: the Decentralized Identity Management (DIM) Wallet. To cover the wallet functionalities in the [E2E Adopter Journey Data exchange](#data-exchange) and [E2E Adopter Journey Portal](#portal), the [SSI DIM Wallet Stub](https://github.com/eclipse-tractusx/ssi-dim-wallet-stub) was added to the umbrella helm chart.

As an intermediate solution - before the SSI DIM Wallet Stub - the [iatp-mock](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/umbrella/charts/iatpmock/Chart.yaml) was added, please see [Precondition for IATP Mock](#precondition-for-iatp-mock) if you'd still like to use it. Please be aware that it doesn't cover the wallet functionalities needed for the [E2E Adopter Journey Portal](#portal) for instance during the onboarding process of a company.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
