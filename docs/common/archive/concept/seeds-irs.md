# Necessary IDP Info

| Attribute | Description |
| -------- | ------- |
| client_id discoveryFinder|The client_id of a technical user with the required role "Dataspace Discovery" |
| client_secret discoveryFinder|The client_secret used for the technical user authentication. |
| discovery_finder_url|Used for looking up the EDC URLs |
| client_id partnersPool|The client_id of a technical user with the required role "BPDM Pool" |
| client_secret partnersPool|The client_secret used for the technical user authentication. |
| partners_pool_url|Used for looking up the manufacturer name to a BPNL |
| client_id semanticHub|The client_id of a technical user with the required role "Semantic Model Management" |
| client_secret semanticHub|The client_secret used for the technical user authentication. |
| semantic_hub_url|Used to obtain available semantic models and their JSON schema |
| oauth_token_url|Used to obtain a Oauth2 Token for the services SemanticHub, Discovery Finder, BPDM Pool |

## EDC Configuration

### Option 1 (managed EDC)

| Attribute | Description |
| -------- | ------- |
| edc_consumer_management_url|Pre-configured EDC instance used by IRS to consume data |
| edc_consumer_management_token|Token to access the management instance |

### Option 2 (self-deployed EDC)

| Attribute | Description |
| -------- | ------- |
| miw_url|Used for retrieving wallet details / edc authentication. |
| client_id miw|The client_id of a technical user with the required role "Identity Wallet Management" |
| client_secret miw|The client_secret used for the technical user authentication. |
| miw_authority_id|If not retrievable by http get request |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

