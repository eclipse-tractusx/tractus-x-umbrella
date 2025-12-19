# Migration Guide

This migration guide is based on the `chartVersion` of the chart. If you don't rely on the provided helm chart, consider the changes of the chart as mentioned below manually.

> [!WARNING]
> Bitnami does change their update and versioning policy starting with 2025-08-28. To install the existing charts with its bitnami dependencies, please consider to manually specify the properties `image.repository` and `image.tag` specifying for the following dependencies:
> 
> - postgresql (image: bitnamilegacy/postgresql:15.4.0-debian-11-r45)
> 
> You have the following options to specify the container image:
> 
> 1. Specify in `values.yaml` below `postgresql`.
> 
> ```yaml
> postgresql: 
>   image: 
>     repository: bitnamilegacy/postgresql
>     tag: 15.4.0-debian-11-r45
> ```
> 
> 2. Set during installation.
> 
> ```bash
> helm install puris -n tractusx-dev/puris \
>   --set postgresql.image.repository=bitnamilegacy/postgresql
>   --set postgresql.image.tag=15.4.0-debian-11-r45
> ```
> 
> Notes:
> 
> - Deploying an older version of the software may have used an older postgresql version. This is NOT applicable for the PURIS charts.
> - The community is working out on how to resolve the issue.
>
## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
