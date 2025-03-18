[![OverarchingRelease](https://img.shields.io/badge/Release_24.08-blue)](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.08/CHANGELOG.md#2408---2024-08-05)

# Eclipse Tractus-X Umbrella

This repository contains an umbrella helm chart designed to simplify the setup and management of the [Catena-X](https://catena-x.net/en/)
automotive dataspace network, leveraging [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) open-source components. It supports end-to-end testing, sandbox environments, and integration with various Catena-X services.

The umbrella helm chart is located in the [charts/umbrella](./charts/umbrella) directory.

## Usage

**Prerequisites & Installation**

For the prerequisites and installing of the umbrella charts please check the [docs](docs/README.md) section.

**Tutorials**

After installing the umbrella charts, you can refer to the [user guides and tutorials sections](docs/user/guides/README.md) for more information about the dataspace network.

## Key Features

- **Automated Setup**: Provides a fully functional network with minimal manual intervention.
- **Modular Subsets**: Includes predefined subsets for specific use cases like data exchange, portal management, and business partner data management.
- **Extensible**: Easily integrates with additional components or custom configurations.
- **Cross-Platform Support**: Tested on Linux, macOS, and partial on Windows systems.

## Release Compatibility

The versions of the [integrated components](docs/user/setup/chart-installation/README.md#available-components) correspond to the **overarching [Release 24.12](https://github.com/eclipse-tractusx/tractus-x-release/blob/24.12/CHANGELOG.md#2412---2024-12-02)**.

## Purpose

The Umbrella Chart is intended for:
1. **Testing**: Run end-to-end tests for Catena-X services.
2. **Sandbox Environments**: Create local environments to evaluate and experiment with Catena-X components.
3. **Development**: Provide a unified setup for contributors and developers working on Tractus-X projects.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).

## License

Distributed under the Apache 2.0 License.
See [LICENSE](./LICENSE) for more information.
