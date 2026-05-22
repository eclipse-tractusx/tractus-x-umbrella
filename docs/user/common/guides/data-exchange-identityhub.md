# Data Exchange with Decentralized IdentityHub Usage

This guide provides instructions for using the Data Exchange with Decentralized IdentityHub configuration of the Umbrella Chart.

## Overview

The Data Exchange with Decentralized IdentityHub enables secure data sharing between participants using decentralized identifiers (DIDs) and verifiable credentials. This configuration demonstrates a decentralized identity architecture where each participant manages their own IdentityHub for credential management and Self-Issued token issuance.

## Involved Components

The following components are part of the Data Exchange with Decentralized IdentityHub subset:

- **EDC Provider**: Eclipse Dataspace Connector acting as a data provider with integrated IdentityHub.
- **EDC Consumer**: Eclipse Dataspace Connector acting as a data consumer with integrated IdentityHub.
- **BDRS Server**: BPN/DID Resolution Service for mapping Business Partner Numbers to Decentralized Identifiers.
- **PostgreSQL**: Database instances for both provider and consumer connectors and IdentityHubs.

## Accessing the Data Exchange

### URLs

- **Provider**:
  ```
  http://provider.local
  http://provider.intranet (management)
  ```
- **Consumer**:
  ```
  http://consumer.local
  http://consumer.intranet (management)
  ```
- **BDRS Server**:
  ```
  http://bdrs-server.tx.test
  ```

### Participant Identifiers

| Participant | BPN | DID |
|-------------|-----|-----|
| **Provider** | BPNL000000000001 | did:web:provider.local:identityhub:BPNL000000000001 |
| **Consumer** | BPNL000000000002 | did:web:consumer.local:identityhub:BPNL000000000002 |
| **Issuer Service** | BPNL000000000003 | did:web:issuerservice.issuance.local:BPNL000000000003 |

## Testing the Data Exchange

You can test and interact with the Data Exchange with Decentralized IdentityHub using the following tools:

### Bruno Collection

Import the Bruno collection for the Umbrella Chart to test predefined APIs:
[Bruno Collection](../../../common/api/README.md).

## Notes

- Ensure all components are running and DNS resolution is correctly configured for `provider.local`, `provider.intranet`, `consumer.local`, `consumer.intranet`, and `bdrs-server.tx.test` domains.
- This configuration uses decentralized identifiers (DIDs) and does not require a central CX-IAM/Keycloak instance.
- Each participant has their own IdentityHub for managing credentials and issuing Self-Issued tokens.
- The configuration uses `did:web` method for DID resolution.
- **Important**: Each EDC instance with integrated IdentityHub must be deployed in a separate namespace to avoid resource conflicts and ensure proper isolation between participants. This limitation will be resolved after IdentityHub version 0.2.0.

For further details, refer to the [Data Exchange Installation Guide](../setup/README.md#data-exchange-subset).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
