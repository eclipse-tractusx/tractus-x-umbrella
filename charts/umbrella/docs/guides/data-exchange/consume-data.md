# Consume Data

> Variables enclosed in {{ }} mean that they are whose content has been obtained from the answers of previous calls.

## 1. Query Catalog

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

## 2. Initiate Negotiation
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

## 3. Get Negotiation By ID

```
curl -L -X GET 'http://dataconsumer-1-controlplane.tx.test/management/v2/contractnegotiations/' \
-H 'X-Api-Key: TEST1'
```
You should be able to see in the response, that the _state_ value is equal to _FINALIZED_.

We get {{contractagreement_id}} from the response.

## 4. Initiate Transfer

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

## 5. Get Transfer by ID

```
curl -L -X GET 'http://dataconsumer-1-controlplane.tx.test/management/v2/transferprocesses/{{transfer_id}}' \
-H 'X-Api-Key: TEST1'
```

You should be able to see in the response that the _state_ value is equal to _STARTED_.

## 6. Validate Transfer

```
curl -L -X GET 'http://dataprovider-submodelserver.tx.test/api/v1/transfers/TEST1/contents'
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://www.apache.org/licenses/LICENSE-2.0).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
