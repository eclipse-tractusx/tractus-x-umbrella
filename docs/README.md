# Umbrella Chart

This umbrella chart provides a foundation for running end-to-end tests or creating sandbox environments of the [Catena-X](https://catena-x.net/en/) automotive dataspace using
[Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) OSS components.

> **Note**
>
> In its current state of development, this chart as well as the following installation guide have been tested on Linux and Mac.
>
> **Linux** is the **preferred platform** to install this chart on, as the network setup with Minikube is very straightforward on Linux.

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

The following table links you to the respective documentations.

## **Table of Contents**
- [Note from R24.05 onwards](user/note-r2405-onwards/README.md)
- [Helm Chart installation including prerequisites](user/setup/README.md)
    - [Quickinstall](user/setup/quickinstall/README.md)
    - [Install Cluster](user/setup/cluster/README.md)
    - [Install Charts](user/setup/chart-installation/README.md)
      - [Released Charts](user/setup/chart-installation/released-chart.md)
      - [Local Charts](user/setup/chart-installation/local-repository.md)
      - [Uninstallation](user/setup/chart-installation/uninstallation.md)
    - [Setup Network](user/setup/network/README.md)
      - [TLS (Optional)](user/setup/network/tls.md)
    - [Semantic Hub Precondition](user/setup/semantic-hub/README.md)
- [Guides](user/guides/README.md)
    - [Data Exchange](user/guides/data-exchange.md)
        - [Data Provider](user/guides/data-exchange/provide-data.md)
        - [Data Consumer](user/guides/data-exchange/consume-data.md)
    - [Portal Usage](user/guides/portal-usage.md)
    - [Database Access](user/guides/database-access.md)
- [API Requests](api/README.md)
- [Test Data Seeding](test-data-seeding/README.md)

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
