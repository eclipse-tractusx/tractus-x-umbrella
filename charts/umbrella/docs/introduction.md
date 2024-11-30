# Introduction

This document provides an overview of the Umbrella Chart and its purpose.

The Umbrella Chart is designed to simplify the setup and management of the [Catena-X](https://catena-x.net/en/) automotive dataspace network, leveraging [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) open-source components. It supports end-to-end testing, sandbox environments, and integration with various Catena-X services.

## Key Features
- **Automated Setup**: Provides a fully functional network with minimal manual intervention.
- **Modular Subsets**: Includes predefined subsets for specific use cases like data exchange, portal management, and business partner data management.
- **Extensible**: Easily integrates with additional components or custom configurations.
- **Cross-Platform Support**: Tested on Linux, macOS, and partial on Windows systems.

## Release Compatibility
The versions of integrated components correspond to:
- **[Release 24.05](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.05/CHANGELOG.md#2405---2024-05-29)**: Current stable release.
- **[Release 24.08](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.08/CHANGELOG.md#2408---2024-08-05)**: Partial upgrades for some components.

## Purpose
The Umbrella Chart is intended for:
1. **Testing**: Run end-to-end tests for Catena-X services.
2. **Sandbox Environments**: Create local environments to evaluate and experiment with Catena-X components.
3. **Development**: Provide a unified setup for contributors and developers working on Tractus-X projects.

## Cluster Setup
- Ensure your cluster meets the updated system requirements:
    - Kubernetes version `>1.24.x`
    - Helm version `3.8+`

## Pre-Requisites

Running this helm chart **requires** a kubernetes cluster (`>1.24.x`), it's recommended to run it on [**Minikube**](https://minikube.sigs.k8s.io/docs/start/).
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following instructions to install the chart as `umbrella` release.

> **Note**
>
> In its current state of development, this chart as well as the following installation guide have been tested on Linux and Mac.
>
> **Linux** is the **preferred platform** to install this chart on, as the network setup with Minikube is very straightforward on Linux.
>
> We are working on testing the chart's reliability on Windows as well and updating the installation guide accordingly.

> **Note**
>
> In its current state of development, this chart as well as the following installation guide have been tested on Linux and Mac.
>
> **Linux** is the **preferred platform** to install this chart on, as the network setup with Minikube is very straightforward on Linux.
>
> We are working on testing the chart's reliability on Windows as well and updating the installation guide accordingly.

For detailed setup instructions, refer to the [Setup Guide](setup/cluster-setup.md).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://www.apache.org/licenses/LICENSE-2.0).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
