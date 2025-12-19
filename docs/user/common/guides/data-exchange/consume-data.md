# Consume Data

In order to be able to consume data, it is necessary to have previously [provided](./provide-data.md).

> **Please** have a look at the `cURL explanation` Notes in the beginning of [Provide Data](provide-data.md) to get more information about cURL. 

This step continues the journey of our data consumer Alice. After the data provider Bob has successfully provided his data as a contract definition in his catalog. Alice will now consume the data.
We will use plain CLI tools (`curl`) for this, but feel free to use graphical tools such as Postman or Insomnia.

>[!WARNING]
>- This works for the HTTP-Pull scenario.
```mermaid
sequenceDiagram
    participant Alice as Alice (Consumer)
    participant EDC_C as Alice's Connector
    participant EDC_P as Bob's Connector
    participant Bob as Bob (Endpoint)

    Alice->>EDC_C: Query Catalog
    EDC_C->>EDC_P: Request Catalog
    EDC_P-->>EDC_P: Identify Datasets based on Access Policies
    EDC_P->>EDC_C: Catalog Response
    EDC_C-->>Alice: Display Assets

    Alice->>EDC_C: Negotiate Contract
    EDC_C->>EDC_P: Contract Offer
    EDC_P-->>EDC_P: Validate Credentials and Finalize Contract
    EDC_C->>EDC_P: Check Status of Contract (polling until state is Finalized)
    EDC_P-->>EDC_C: Status of Contract
    Alice->>EDC_C: Data Transfer Request
    EDC_C->>EDC_P: Data Transfer Request
    Note over EDC_P: Include auth token & endpoint
    EDC_P->>EDC_P: Create EDR
    EDC_P-->>EDC_C: EDR Response
    Alice->>EDC_C: Query EDRS Response
    EDC_C-->>Alice: EDR Response

    Alice->>EDC_P_DP: Data Request
    Note over Alice,EDC_P: With token from EDR
    EDC_P_DP->>Bob: Fetch Data
    Bob-->>EDC_P_DP: Return Data
    EDC_P_DP-->>Alice: Transfer Data
    EDC_C-->>Alice: Deliver Data
```
This diagram illustrates the three main phases of data consumption:
1. **Catalog Query**: Alice discovers available assets
2. **Contract Negotiation**: Alice negotiates access terms
3. **Data Transfer**: Alice receives the requested data

The default life time of the EDR token is 300s, its recommended for manual tests to extend the expiration time. 

## Step 1: Request the catalog

To see Bob's data offerings, Alice must request access to his catalog. The catalog shows all the assets that Alice can consume from Bob.

### Catalog request (Alice)

```bash
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v3/catalog/request' \
  -H 'Content-Type: application/json' \
  -H 'X-Api-Key: TEST1' \
  --data-raw '{
    "@context": [
      {
        "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
      }
    ],
    "@type": "CatalogRequest",
    "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp/2025-1",
    "counterPartyId": "BPNL00000003AYRE",
    "protocol": "dataspace-protocol-http:2025-1",
    "querySpec": {
      "offset": 0,
      "limit": 50,
      "sortOrder": "DESC",
      "sortField": "fieldName",
      "filterExpression": []
    }
  }' | jq
```

### Catalog response

We have already learned about the response of a catalog request in the [Provide Data](provide-data.md) guide. The response contains a list of assets that Alice can consume from Bob.

The response (here just an extract) will contain the `@id` `200` of the asset that Alice wants to consume, but also the `@id` `MjAw:MjAw:Y2ZjMzdlNmUtODAwNi00NGJjLWJhMWYtNjJkOWIzZWM0ZTQ3` of the offer
that Alice needs to reference in the negotiation.

```json
{
  "@id": "200",
  "@type": "dcat:Dataset",
  "odrl:hasPolicy": {
    "@id": "MjAw:MjAw:Y2ZjMzdlNmUtODAwNi00NGJjLWJhMWYtNjJkOWIzZWM0ZTQ3",
    "@type": "odrl:Offer",
    "odrl:permission": {
      "odrl:action": {
        "odrl:type": "USE"
      },
      "odrl:constraint": {
        "odrl:or": {
          "odrl:leftOperand": "BusinessPartnerNumber",
          "odrl:operator": {
            "@id": "odrl:eq"
          },
          "odrl:rightOperand": "BPNL00000003AZQP"
        }
      }
    }
  }
}
```

## Step 2: Initiate an edr

To consume the data, Alice uses the `OFFER_ID` `MjAw:MjAw:Y2ZjMzdlNmUtODAwNi00NGJjLWJhMWYtNjJkOWIzZWM0ZTQ3` from the previous catalog response and the target `ASSET_ID` `200` to initiate an [EDR](https://github.com/eclipse-tractusx/tractusx-edc/blob/main/docs/usage/management-api-walkthrough/07_edrs.md).

### EDR request

```bash
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v3/edrs' \
  -H 'Content-Type: application/json' \
  -H 'X-Api-Key: TEST1' \
  --data-raw '{
    "@context": [
      "http://www.w3.org/ns/odrl.jsonld",
      "https://w3id.org/catenax/2025/9/policy/context.jsonld",
      {
        "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
      }
    ],
    "@type": "ContractRequest",
    "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp",
    "protocol": "dataspace-protocol-http:2025-1",
    "policy": {
      "@id": "{{OFFER_ID}}",
      "@type": "Offer",
      "assigner": "did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AYRE",
      "target": "200",
      "permission": [
        {
          "action": "use",
            "constraint": [
              {
                "and": [
                  {
                    "leftOperand": "Membership",
                    "operator": "eq",
                    "rightOperand": "active"
                  },
                  {
                    "leftOperand": "FrameworkAgreement",
                    "operator": "eq",
                    "rightOperand": "DataExchangeGovernance:1.0"
                  },
                  {
                    "leftOperand": "UsagePurpose",
                    "operator": "isAnyOf",
                    "rightOperand": "cx.core.industrycore:1"
                  }
                ]
              }
            ]
        }
      ],
      "prohibition": [],
      "obligation": []
    },
    "callbackAddresses": []
  }' | jq
```

### EDR response

The response also includes the `@id` `4b260501-ae2f-46f4-9efc-01ba5a0b3d96` of the EDR, which Alice can use to get the EDR and more information.

```json
{
  "@type": "IdResponse",
  "@id": "4b260501-ae2f-46f4-9efc-01ba5a0b3d96",
  "createdAt": 1732726185609,
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
    "edc": "https://w3id.org/edc/v0.0.1/ns/",
    "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
    "tx-auth": "https://w3id.org/tractusx/auth/",
    "cx-policy": "https://w3id.org/catenax/policy/",
    "odrl": "http://www.w3.org/ns/odrl/2/"
  }
}
```

## Step 3: Query cached edrs

Alice now queries cached EDRs using the {{CONTRACT_NEGOTIATION_ID}} `4b260501-ae2f-46f4-9efc-01ba5a0b3d96` from the previous response.

### Query edrs request

```shell
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v3/edrs/request' \
  -H 'Content-Type: application/json' \
  -H 'X-Api-Key: TEST1' \
  --data-raw '{
    "@context": { "@vocab": "https://w3id.org/edc/v0.0.1/ns/" },
    "@type": "QuerySpec",
    "filterExpression": [
      {
        "operandLeft": "contractNegotiationId",
        "operator": "=",
        "operandRight": "{{CONTRACT_NEGOTIATION_ID}}"
      }
    ]
  }' | jq
```

### Query edrs response

The response will contain the EDR with the `@id` `bdd4af10-9e4a-4796-b4b7-7ecdf91a533a` and the `transferProcessId` `bdd4af10-9e4a-4796-b4b7-7ecdf91a533a`, which is important for the next step. of the contract agreement.

```json
{
  "@id": "bdd4af10-9e4a-4796-b4b7-7ecdf91a533a",
  "@type": "EndpointDataReferenceEntry",
  "providerId": "BPNL00000003AYRE",
  "assetId": "200",
  "agreementId": "2ece6f45-ff09-4417-b5a9-a92a1849f1d0",
  "transferProcessId": "bdd4af10-9e4a-4796-b4b7-7ecdf91a533a",
  "createdAt": 1732726189831,
  "contractNegotiationId": "4b260501-ae2f-46f4-9efc-01ba5a0b3d96",
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
    "edc": "https://w3id.org/edc/v0.0.1/ns/",
    "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
    "tx-auth": "https://w3id.org/tractusx/auth/",
    "cx-policy": "https://w3id.org/catenax/policy/",
    "odrl": "http://www.w3.org/ns/odrl/2/"
  }
}
```

## Step 4: Get authorization details

Alice uses the {{TRANSFER_PROCESS_ID}} `bdd4af10-9e4a-4796-b4b7-7ecdf91a533a` to get authorization details.

### Authorization request

```bash
curl -L -X GET 'http://dataconsumer-1-controlplane.tx.test/management/v3/edrs/{{TRANSFER_PROCESS_ID}}/dataaddress?auto_refresh=true' \
  -H 'X-Api-Key: TEST1' | jq
```

### Authorization response


The response will contain the authorization details, including the `endpoint` and `authorization`which are needed to fetch the data via the data plane.

```json
{
  "@type": "DataAddress",
  "endpointType": "https://w3id.org/idsa/v4.1/HTTP",
  "tx-auth:refreshEndpoint": "http://dataprovider-dataplane.tx.test/api/public/token",
  "tx-auth:audience": "did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AZQP",
  "type": "https://w3id.org/idsa/v4.1/HTTP",
  "endpoint": "http://dataprovider-dataplane.tx.test/api/public",
  "tx-auth:refreshToken": "eyJraWQiOiJ0b2tlblNpZ25lclB1YmxpY0tleSIsImFsZyI6IlJTMjU2In0.eyJleHAiOjE3MzI3MjY0ODksImlhdCI6MTczMjcyNjE4OSwianRpIjoiODA2OTAwYmQtNGY4MS00MzhmLTgyMjYtZDc2ZjkzMmY2MjI1In0.JpTIrOJv609vX86i-y-O8sQcKoTJcWvipC6jyBgWqcEIMWm4dmm4T72z-Z68l1X7QnVq1Ak8JB-fA05ONNL1JjU0W7j6rJK01M2Xo641RpecimxuFhlnld55CPks2wRbbbzHADn8kpqRf2dtNrnsiuRsnzAi6KAkFAEHLB7eLjceNbkk6df3hJrLfnn0DZ6M-OR0O05SgtEyHFsyMpf4OALQwVREIkC7LBTWn7nYCpmzK4ilrL3eM5ZRrbweQ96Tbwi-rfPfp-ptnelO_GGnqzyQef2DN5Eg4P5QZV4QX62Bw0eoYVncgCP6ZKibymnlASG0xHwgEJitu3ZSxBXt-w",
  "tx-auth:expiresIn": "300",
  "authorization": "eyJraWQiOiJ0b2tlblNpZ25lclB1YmxpY0tleSIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJCUE5MMDAwMDAwMDNBWVJFIiwiYXVkIjoiQlBOTDAwMDAwMDAzQVpRUCIsInN1YiI6IkJQTkwwMDAwMDAwM0FZUkUiLCJleHAiOjE3MzI3MjY0ODksImlhdCI6MTczMjcyNjE4OSwianRpIjoiODRkZDIxOGItMzk1ZC00YmExLTg2OWUtOWYzMjI3ZWM0NWFlIn0.jTKEv8Fh75W1JOwrFUo1wyLdUOyBn3g500dWNUbaEC_bgASPImXfXnY3rhIVr_hrFY-anJIB_a6SkpTWb7lycCh2dcMaOmUVgmdKTcEvTr2blAXD_WUZTQYxHDVsMuPXDbX-30tYM4KVPOyemfe7IreB38n104j_SLo2Dr1BrbN9xU7mUm6DeKv1oi0TFRxnmhwnRx4hK1eBYIO-FuA9h1RDvfLWXW5yF55KkkrRTjX2HKqVPAtHInMZBRDhqB298N_VLpwQMtg9nkElzNWIUqEV4zQ1YLSsGNLSxog7JwuL3Tvy1VCOkzDkr6K89Z4IWEF0GzPjXO6Z-li_Vv7DVw",
  "tx-auth:refreshAudience": "did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AZQP",
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
    "edc": "https://w3id.org/edc/v0.0.1/ns/",
    "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
    "tx-auth": "https://w3id.org/tractusx/auth/",
    "cx-policy": "https://w3id.org/catenax/policy/",
    "odrl": "http://www.w3.org/ns/odrl/2/"
  }
}
```

## Step 5: Fetch data

Using the {{ENDPOINT}} and {{TOKEN}} from the response, Alice fetches the data. In our example the `uuid` `urn:uuid:b77c6d51-cd1f-4c9d-b5d4-091b22dd306b` for the data is already known. In
real life you would receive this information from the digital twin registry as an endpoint in the submodelDescriptors.

### Fetch data request

```bash
curl -L -X GET '{{ENDPOINT}}/urn:uuid:b77c6d51-cd1f-4c9d-b5d4-091b22dd306b' \
  -H 'Authorization: {{TOKEN}}' | jq
```

### Fetch data response

```json
{
  "parentParts": [
    {
      "validityPeriod": {
        "validFrom": "2023-03-21T08:47:14.438+01:00",
        "validTo": "2024-08-02T09:00:00.000+01:00"
      },
      "parentCatenaXId": "urn:uuid:0733946c-59c6-41ae-9570-cb43a6e4c79e",
      "quantity": {
        "quantityNumber": 2.5,
        "measurementUnit": "unit:litre"
      },
      "createdOn": "2022-02-03T14:48:54.709Z",
      "lastModifiedOn": "2022-02-03T14:48:54.709Z"
    }
  ],
  "catenaXId": "urn:uuid:2c57b0e9-a653-411d-bdcd-64787e9fd3a7"
}
```

> **Congratulations**
> You have successfully consumed data from Bob.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
