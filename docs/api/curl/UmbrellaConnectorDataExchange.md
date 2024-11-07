## Data Exchange Tutorial

Once the data space has been launched (please see [charts/umbrella/README.md](../../../charts/umbrella/README.md) until **Install --> Data Exchange Subset**), we will execute the following steps/calls to perform the communication between the components.

> Variables enclosed in {{ }} mean that they are whose content has been obtained from the answers of previous calls.

### 1. Create Asset

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

### 2. Get Asset by ID

To check if the asset is correctly created.

```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v3/assets/200' \
-H 'X-Api-Key: TEST2'
```

### 3. Create Policy

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
              "odrl:leftOperand": "BusinessPartnerNumber",
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

### 4. Get Policies by ID

To check if the Policies are correctly created.
```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v2/policydefinitions/200' \
-H 'X-Api-Key: TEST2'
```

### 5. Create Contract Definition

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

### 6. Get Contract Definition by ID

To check if the Contract Definition is correctly executed
```
curl -L -X GET 'http://dataprovider-controlplane.tx.test/management/v2/contractdefinitions/200' \
-H 'X-Api-Key: TEST2'
```

### 7. Query Catalog

```
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v2/catalog/request' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST1' \
--data-raw '{
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
  },
  "@type": "CatalogRequest",
  "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp",
  "counterPartyId": "BPNL00000003AYRE",
  "protocol": "dataspace-protocol-http",
  "querySpec": {
    "offset": 0,
    "limit": 50
  }
}'
```

We get the {{offer_id}} from the response.

### 8. Initiate Negotiation
```
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v2/contractnegotiations' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST1' \
--data-raw '{
	"@context": {
		"@vocab": "https://w3id.org/edc/v0.0.1/ns/"
	},
	"@type": "NegotiationInitiateRequestDto",
	"counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp",
	"protocol": "dataspace-protocol-http",
	"policy": {
		"@context": "http://www.w3.org/ns/odrl.jsonld",
		"@type": "odrl:Offer",
		"@id": "",
         "assigner": "BPNL00000003AYRE",
		"permission": {
			"odrl:target": "200",
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
		},
		"prohibition": [],
		"obligation": [],
		"target": "200"
	}
}'
```

We get {{negotiation_id}} from the response.

### 9. Get Negotiation By ID

```
curl -L -X GET 'http://dataconsumer-1-controlplane.tx.test/management/v2/contractnegotiations/' \
-H 'X-Api-Key: TEST1'
```
You should be able to see in the response, that the _state_ value is equal to _FINALIZED_.

We get {{contractagreement_id}} from the response.

### 10. Initiate Transfer

```
curl -L -X POST 'http://dataconsumer-1-controlplane.tx.test/management/v2/transferprocesses' \
-H 'Content-Type: application/json' \
-H 'X-Api-Key: TEST1' \
--data-raw '{
  "@context": {
    "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
  },
  "@type": "TransferRequest",
  "protocol": "dataspace-protocol-http",
  "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp",
  "contractId": "",
  "assetId": "200",
  "transferType": "HttpData-PULL",
  "dataDestination":  {
    "type": "HttpProxy"
  },
  "connectorId": "BPNL00000003AZQP",
  "callbackAddresses": [
    {
      "transactional": true,
      "uri": "http://dataprovider-submodelserver.tx.test/api/v1/transfers"
    }
  ]
}'
```

We get {{transfer_id}} from the response

### 11. Get Transfer by ID

```
curl -L -X GET 'http://dataconsumer-1-controlplane.tx.test/management/v2/transferprocesses/{{transfer_id}}' \
-H 'X-Api-Key: TEST1'
```

You should be able to see in the response that the _state_ value is equal to _STARTED_.

### 12. Validate Transfer

```
curl -L -X GET 'http://dataprovider-submodelserver.tx.test/api/v1/transfers/TEST1/contents'
```
