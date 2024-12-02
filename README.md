[![OverarchingRelease](https://img.shields.io/badge/Release_24.08-blue)](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.08/CHANGELOG.md#2408---2024-08-05)

# Eclipse Tractus-X Umbrella

This repository is the homebase for all end-to-end test automation efforts at Eclipse Tractus-X.
It contains an umbrella helm chart to deploy a sandbox Catena-X dataspace based on the Tractus-X OSS components, as well as automated tests and workflows to verify the e2e use cases and the compatibility of the OSS components and versions.

## Umbrella Helm Chart

This document provides an overview of the Umbrella Chart and its purpose. The Umbrella Chart is designed to simplify the setup and management of the [Catena-X](https://catena-x.net/en/)
automotive dataspace network, leveraging [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) open-source components. It supports end-to-end testing, sandbox environments, and integration with various Catena-X services.

For details and further information, please refer to the helm chart specific [README](./charts/umbrella/README.md).

Also have a look in the [docs](docs/README.md) section to get more information about the user manuals and guides.

### Key Features
- **Automated Setup**: Provides a fully functional network with minimal manual intervention.
- **Modular Subsets**: Includes predefined subsets for specific use cases like data exchange, portal management, and business partner data management.
- **Extensible**: Easily integrates with additional components or custom configurations.
- **Cross-Platform Support**: Tested on Linux, macOS, and partial on Windows systems.

### Release Compatibility

The versions of integrated components correspond to the **overarching [Release 24.08](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.08/CHANGELOG.md#2408---2024-08-05)** 

### Purpose

The Umbrella Chart is intended for:
1. **Testing**: Run end-to-end tests for Catena-X services.
2. **Sandbox Environments**: Create local environments to evaluate and experiment with Catena-X components.
3. **Development**: Provide a unified setup for contributors and developers working on Tractus-X projects.

### Cluster Setup

- Ensure your cluster meets the updated system requirements:
    - Kubernetes version `>1.24.x`
    - Helm version `3.8+`

### Pre-Requisites

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

## Contributing

Thank you for your interest in contributing to the Umbrella Chart project! Your contributions are vital to the success and growth of the project.
Before contributing, make sure, you read and understand our [contributing guidelines](CONTRIBUTING.md).

### How to Contribute

We welcome contributions in the following areas:

- **Bug Reports**: Identify and report bugs or issues in the project.
- **Feature Requests**: Suggest enhancements or new features.
- **Code Contributions**: Provide fixes, improvements, or new functionality.
- **Documentation**: Improve existing documentation or add new guides and tutorials.

### Contribution Principles

- **Avoid Company-Specific Setup**: Contributions should not include configurations, dependencies, or tools specific to a single organization.
- **Avoid Proprietary Tooling**: Do not include components or infrastructure that require subscriptions, licenses, or proprietary tools.
- **Be Vendor and Cloud Agnostic**: Ensure that your contributions are neutral and compatible with a wide range of vendors, platforms, and cloud providers.

### Best Practices

- **Write Documentation**: Ensure that new features or changes are well-documented for others to understand and use.
- **Collaborate**: Engage with the community through issues and discussions to align your contributions with the project's vision.
- **Iterate**: Start with small, incremental changes to allow for easier review and feedback.

### Resources

- [Code of Conduct](CODE_OF_CONDUCT.md): Understand the behavior expected in our community.

We appreciate every contribution and look forward to collaborating with you!

