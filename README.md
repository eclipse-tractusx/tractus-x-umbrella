[![OverarchingRelease](https://img.shields.io/badge/Release_25.06-blue)](https://github.com/eclipse-tractusx/tractus-x-release/blob/25.06/CHANGELOG.md#2506---2025-06-16)

# Eclipse Tractus-X Umbrella

This repository contains an umbrella helm chart designed to simplify the setup and management of the [Catena-X](https://catena-x.net/en/)
automotive dataspace network, leveraging [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) open-source components. It supports end-to-end testing, sandbox environments, and integration with various Catena-X services.

The umbrella helm chart is located in the [charts/umbrella](./charts/umbrella) directory.

Have a look in the [docs](/docs) section for user manuals and guides.

## Usage

Execute the following steps:

1. [Cluster Setup](/docs/user/setup/)
2. [Network Setup](/docs/user/network/)
3. [Installation](/docs/user/installation/)

After the installation, you can refer to the [user guides and tutorials sections](/docs/user/guides/).

## Key Features

- **Automated Setup**: Provides a fully functional network with minimal manual intervention.
- **Modular Subsets**: Includes predefined subsets for specific use cases like data exchange, portal management, and business partner data management.
- **Extensible**: Easily integrates with additional components or custom configurations.
- **Cross-Platform Support**: Tested on Linux, macOS, and partial on Windows systems.

## Release Compatibility

The versions of the [integrated components](/docs/user/installation/README.md#available-components) correspond to the overarching **[Release 25.06](https://github.com/eclipse-tractusx/tractus-x-release/blob/25.06/CHANGELOG.md#2506---2025-06-16)** (Updating to Release 25.09)

## Purpose

The Umbrella Chart is intended for:

1. **Testing**: Run end-to-end tests for Catena-X services.
2. **Sandbox Environments**: Create local environments to evaluate and experiment with Catena-X components.
3. **Development**: Provide a unified setup for contributors and developers working on Tractus-X projects.

## Cluster Setup

- Ensure your cluster meets the updated system requirements:
  - Kubernetes version `>1.24.x`
  - Helm version `3.8+`

For detailed setup instructions, refer to the [Setup Guide](/docs/user/setup/README.md).

## Prerequisites

Running this helm chart **requires** a kubernetes cluster (`>1.24.x`), it's recommended to run it on [**Minikube**](https://minikube.sigs.k8s.io/docs/start/).
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following instructions to install the chart as `umbrella` release.

> **Note**
>
> In its current state of development, this chart as well as the following installation guide have been tested on Linux and Mac.
>
> **Linux** is the **preferred platform** to install this chart on, as the network setup with Minikube is very straightforward on Linux.

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

For detailed setup instructions, refer to the [Setup Guide](/docs/user/setup/README.md).

## Testing GitHub workflows locally

If you want to try out your new or improved GitHub workflow locally, before pushing, you can try to use
[act](https://github.com/nektos/act). Follow the official [installation instructions](https://github.com/nektos/act#installation)
for your OS/package manager to set it up on your machine.

There is also plenty of documentation on how to use act and simulate events, that would trigger workflow runs on GitHub.
Some workflows might run into issues, when running them locally. This might be caused by missing values for
`${{ github.event }}` references. To fix this, you can provide your own [event](https://github.com/nektos/act#installation)
as `.json` file. There are already examples present in the [/.act](.act) directory.

An local example run via `act` could look like the following: `act -e .act/pr_event.json pull_request`

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).

## License

Distributed under the Apache 2.0 License.
See [LICENSE](./LICENSE) for more information.
