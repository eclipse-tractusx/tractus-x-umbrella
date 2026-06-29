# API Requests for Data Exchange

This document provides information about API requests for the Data Exchange.

Two flows are covered &mdash; pick the one that matches the umbrella profile you deployed:

| Profile | Recommended? | Bruno collection | Console / curl guide |
|---|---|---|---|
| **Decentralized IdentityHub** (`values-adopter-decentralized-identityhub.yaml`) | ✅ Default since Release 25.12 | [Data-exchange-decentralized-identityhub](./bruno/Data-exchange-decentralized-identityhub) | [Data Exchange with Decentralized IdentityHub](../../user/common/guides/data-exchange-identityhub.md) |
| **Centralized Data Exchange** (`values-adopter-data-exchange.yaml`) | Legacy | [Umbrella-bru](./bruno/Umbrella-bru) | [Provide data](../../user/common/guides/data-exchange/provide-data.md) · [Consume data](../../user/common/guides/data-exchange/consume-data.md) |

## Bruno

Both collections are provided in `.bru` format and can be opened directly with
[Bruno](https://www.usebruno.com/):

- [Data-exchange-decentralized-identityhub](./bruno/Data-exchange-decentralized-identityhub) &mdash; provider/consumer flow plus issuance against the IssuerService, targeting the `*.local` / `*.intranet` hostnames used by the IdentityHub profile.
- [Umbrella-bru](./bruno/Umbrella-bru) &mdash; original Alice/Bob data-exchange collection for the legacy centralized profile.

## Curl

Step-by-step console tutorials covering the same flows:

- [Decentralized IdentityHub flow](../../user/common/guides/data-exchange-identityhub.md) &mdash; participant identifiers (BPNs / DIDs) and the end-to-end exchange against `provider.local` / `consumer.local`.
- Legacy centralized flow: [provide data](../../user/common/guides/data-exchange/provide-data.md) and [consume data](../../user/common/guides/data-exchange/consume-data.md).

## NOTICE

This work is licensed under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

* SPDX-License-Identifier: Apache-2.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
