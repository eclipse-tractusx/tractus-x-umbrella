# Provide Data

> Variables enclosed in {{ }} mean that they are whose content has been obtained from the answers of previous calls.

## 1. Create Asset

```
curl -L -X POST 'http://dataprovider-controlplane.tx.test/management/v3/assets' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST2' \
--data-raw '{
  "@context": {},
  "@id": "200",
  "properties": {
    "description": "Product EDC Demo Asset"
  },
  "dataAddress": {
    "@type": "DataAddress",
    "type": "HttpData",
    "baseUrl": "http://dataprovider-submodelserver.tx.test/200"
  }
}'
```

## 2. Get Asset by ID

To check if the asset is correctly created.

```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v3/assets/200' \
-H 'X-Api-Key: TEST2'
```

## 3. Create Policy

```
curl -L -X POST 'http://dataprovider-controlplane.tx.test/management/v2/policydefinitions' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST2' \
--data-raw '{
  "@context": {
    "odrl": "http://www.w3.org/ns/odrl/2/"
  },
  "@type": "PolicyDefinitionRequestDto",
  "@id": "200",
  "policy": {
    "@type": "odrl:Set",
    "odrl:permission": [
      {
        "odrl:action": "USE",
        "odrl:constraint": {
          "@type": "LogicalConstraint",
          "odrl:or": [
            {
              "@type": "Constraint",
              "odrl:leftOperand": {
                "@id": "BusinessPartnerNumber"
              },
              "odrl:operator": {
                "@id": "odrl:eq"
              },
              "odrl:rightOperand": "BPNL00000003AZQP"
            }
          ]
        }
      }
    ]
  }
}'
```

## 4. Get Policies by ID

To check if the Policies are correctly created.
```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v2/policydefinitions/200' \
-H 'X-Api-Key: TEST2'
```

## 5. Create Contract Definition

```
curl -L -X POST 'http://dataprovider-controlplane.tx.test/management/v2/contractdefinitions' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST2' \
--data-raw '{
  "@context": {},
  "@id": "200",
  "@type": "ContractDefinition",
  "accessPolicyId": "200",
  "contractPolicyId": "200",
  "assetsSelector": {
    "@type": "CriterionDto",
    "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
    "operator": "=",
    "operandRight": "200"
  }
}'
```

## 6. Get Contract Definition by ID

To check if the Contract Definition is correctly executed
```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v2/contractdefinitions/200' \
-H 'X-Api-Key: TEST2'
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
