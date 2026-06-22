# Data Exchange Usage

This guide provides instructions for using the Data Exchange subset of the Umbrella Chart.

## Overview

The Data Exchange subset enables secure and efficient data sharing between participants in the Catena-X ecosystem. It includes components such as Data Providers, Data Consumers, and supporting services.

## Involved Components

The following components are part of the Data Exchange subset:

- **Data Provider**: Manages data sharing capabilities for a participant.
- **Data Consumer**: Enables participants to request and consume data from providers.
- **pgAdmin4**: Provides database management functionality for underlying services.

## Accessing the Data Exchange

### URLs

- **Data Provider**:
  ```
  http://dataprovider-dataplane.tx.test
  ```
- **Data Consumer 1**:
  ```
  http://dataconsumer-1-dataplane.tx.test
  ```
- **Data Consumer 2** (if enabled):
  ```
  http://dataconsumer-2-dataplane.tx.test
  ```

## Testing the Data Exchange

You can test and interact with the Data Exchange subset using the following tools:

### 1. Bruno Collection

Import the Bruno collection for the Umbrella Chart to test predefined APIs:
[Bruno Collection](../../../common/api/README.md).

### 2. Curl Commands

Follow the Curl Steps for direct interaction with the APIs to:
- [Provide data as a Data Provider](data-exchange/provide-data.md).
- [Request and consume data as a Data Consumer](data-exchange/consume-data.md).

## Notes

- Ensure all components are running and DNS resolution is correctly configured for the `*.tx.test` domains.
- Refer to the [Cluster Setup Guide](../setup/cluster) if there are issues with service connectivity.
- If additional data consumers are required, enable `dataconsumerTwo` in the `values.yaml` file and redeploy the chart.

For further details, refer to the [Data Exchange Installation Guide](../setup/README.md#data-exchange-subset).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
