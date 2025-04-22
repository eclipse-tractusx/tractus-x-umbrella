#!/usr/bin/python

# #############################################################################
# Copyright (c) 2022,2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# Copyright (c) 2021,2024 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
# #############################################################################

import argparse
import json
import math
import time
import uuid
from copy import copy

import requests
from requests.adapters import HTTPAdapter, Retry


def create_submodel_payload(json_payload):
    return json.dumps(json_payload)


def create_edc_asset_payload(submodel_url_, asset_id_):
    return json.dumps({
        "@context": edc_context(),
        "@id": f"{asset_id_}",
        "edc:properties": {
            "edc:description": "Umbrella EDC Test Asset",
            "edc:id": f"{asset_id_}",
        },
        "edc:dataAddress": {
            "@type": "edc:DataAddress",
            "edc:type": "HttpData",
            "edc:baseUrl": f"{submodel_url_}",
            "edc:proxyPath": "true",
            "edc:proxyBody": "false",
            "edc:proxyMethod": "false",
            "edc:proxyQueryParams": "false"
        }
    })


def create_edc_registry_asset_payload(registry_url_, asset_prop_id_):
    return json.dumps({
        "@context": edc_context(),
        "@id": f"{asset_prop_id_}",  # DTR-EDC-instance-unique-ID
        "edc:properties": {
            "dct:type": {
                "@id": "https://w3id.org/catenax/taxonomy#DigitalTwinRegistry"
            },
            "cx-common:version": "3.0",
            "edc:description": "Digital Twin Registry Endpoint",
            "edc:id": f"{asset_prop_id_}",  # DTR-EDC-instance-unique-ID
            "edc:type": "data.core.digitalTwinRegistry"
        },
        "edc:dataAddress": {
            "@type": "edc:DataAddress",
            "edc:type": "HttpData",
            "edc:baseUrl": f"{registry_url_}",
            "edc:proxyPath": "true",
            "edc:proxyMethod": "true",
            "edc:proxyQueryParams": "true",
            "edc:proxyBody": "true",
            "edc:contentType": "application-json"
        }
    })


def edc_context():
    return {
        "dct": "http://purl.org/dc/terms/",
        "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
        "edc": "https://w3id.org/edc/v0.0.1/ns/",
        "dcat": "https://www.w3.org/ns/dcat/",
        "odrl": "http://www.w3.org/ns/odrl/2/",
        "dspace": "https://w3id.org/dspace/v0.8/",
        "cx-common": "https://w3id.org/catenax/ontology/common#"
    }


def create_edc_contract_definition_payload(edc_policy_id_, asset_prop_id_):
    return json.dumps({
        "@context": edc_context(),
        "@type": "ContractDefinition",
        "accessPolicyId": f"{edc_policy_id_}",
        "contractPolicyId": f"{edc_policy_id_}",
        "assetsSelector": {
            "@type": "CriterionDto",
            "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
            "operator": "=",
            "operandRight": f"{asset_prop_id_}"
        }
    }
    )


def create_aas_shell_3_0(global_asset_id_, id_short_, identification_, specific_asset_id_, submodel_descriptors_):
    return json.dumps({
        "description": [],
        "globalAssetId": global_asset_id_,
        "idShort": id_short_,
        "id": identification_,
        "specificAssetIds": specific_asset_id_,
        "submodelDescriptors": submodel_descriptors_
    })


def create_submodel_descriptor_3_0(id_short_, identification_, semantic_id_, dataplane_asset_address_, asset_id_,
                                   endpoint_):
    return json.dumps(
        {
            "description": [],
            "idShort": id_short_,
            "id": identification_,
            "semanticId": {
                "type": "ExternalReference",
                "keys": [
                    {
                        "type": "GlobalReference",
                        "value": semantic_id_
                    }
                ]
            },
            "endpoints": [
                {
                    "interface": "SUBMODEL-3.0",
                    "protocolInformation": {
                        "href": dataplane_asset_address_,
                        "endpointProtocol": "HTTP",
                        "endpointProtocolVersion": ["1.1"],
                        "subprotocol": "DSP",
                        "subprotocolBody": f"id={asset_id_};dspEndpoint={endpoint_}",
                        "subprotocolBodyEncoding": "plain",
                        "securityAttributes": [
                            {
                                "type": "NONE",
                                "key": "NONE",
                                "value": "NONE"
                            }
                        ]
                    }
                }
            ]
        }
    )


def print_response(response_):
    print(response_)
    if response_.status_code > 205:
        print(response_.text)
    if response_.status_code in [404, 401] or response_.status_code >= 500:
        raise Exception("Failed to call service")


def check_url_args(submodel_server_upload_urls_, submodel_server_urls_, edc_upload_urls_, edc_urls_, dataplane_urls_,
                   edc_bpns_):
    nr_of_submodel_server_upload_urls = len(submodel_server_upload_urls_)
    nr_of_submodel_server_urls = len(submodel_server_urls_)
    if nr_of_submodel_server_upload_urls != nr_of_submodel_server_urls:
        raise ArgumentException(
            f"Number and order of submodelserver upload URLs '{submodel_server_upload_urls_}' "
            f"has to match number and order Number and order of submodelserver URLs '{submodel_server_urls_}'")
    nr_of_edc_upload_urls = len(edc_upload_urls_)
    nr_of_edc_urls = len(edc_urls_)
    if nr_of_edc_upload_urls != nr_of_edc_urls:
        raise ArgumentException(
            f"Number and order of edc upload URLs '{edc_upload_urls_}' has to match number and order of edc URLs "
            f"'{edc_urls_}'")
    nr_of_edc_bpns = len(edc_bpns_)
    if nr_of_edc_urls != nr_of_edc_bpns:
        raise ArgumentException(
            f"Number and order of edc URLs '{nr_of_edc_urls}' has to match number and order of edc BPNs "
            f"'{nr_of_edc_bpns}'")
    if nr_of_submodel_server_urls != nr_of_edc_urls:
        raise ArgumentException(
            f"Number and order of edc URLs '{edc_urls_}' has to match number and order of submodelserver URLS "
            f"'{submodel_server_urls_}'")
    nr_of_dataplane_urls = len(dataplane_urls_)
    if nr_of_dataplane_urls != nr_of_edc_urls:
        raise ArgumentException(
            f"Number and order of edc controlplane URLs '{edc_urls_}' has to match number and order of edc dataplane "
            f"URLS'{submodel_server_urls_}'")


class ArgumentException(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass


def create_policy(policy_, edc_upload_url_, edc_policy_path_, headers_, session_):
    url_ = edc_upload_url_ + edc_policy_path_
    print(f"Create policy {policy_['@id']} on EDC {url_}")
    response_ = session_.request(method="GET", url=f"{url_}/{policy_['@id']}", headers=headers_)
    if response_.status_code == 200 and response_.json():
        print(f"Policy {policy_['@id']} already exists. Skipping creation.")
    else:
        response_ = session_.request(method="POST", url=url_, headers=headers_, data=json.dumps(policy_))
        print(response_)
        if response_.status_code > 205:
            print(response_.text)
        else:
            print(f"Successfully created policy {response_.json()['@id']}.")


def create_registry_asset(edc_upload_urls_, edc_bpns_, edc_asset_path_, edc_contract_definition_path_, catalog_path_, header_,
                          session_, edc_urls_, policy_, registry_asset_id_, aas_url_):
    for edc_upload_url_ in edc_upload_urls_:
        index = edc_upload_urls_.index(edc_upload_url_)
        edc_url_ = edc_urls_[index]
        edc_bpn_ = edc_bpns_[index]
        print(edc_url_)
        print(edc_upload_url_)

        catalog_url_ = edc_upload_url_ + catalog_path_
        payload_ = {
            "@context": edc_context(),
            "edc:protocol": "dataspace-protocol-http",
            "edc:counterPartyAddress": f"{edc_url_}/api/v1/dsp",
            "edc:counterPartyId": f"{edc_bpn_}",
            "edc:querySpec": {
                "edc:filterExpression": {
                    "@type": "edc:Criterion",
                    "edc:operandLeft": "https://w3id.org/edc/v0.0.1/ns/type",
                    "edc:operator": "=",
                    "edc:operandRight": "data.core.digitalTwinRegistry"
                }
            }
        }
        print(f"Query Catalog for registry asset {catalog_url_}")
        response_ = session_.request(method="POST", url=catalog_url_, headers=header_, data=json.dumps(payload_))
        print_response(response_)
        asset_url_ = edc_upload_url_ + edc_asset_path_
        print(response_.status_code)
        catalog_response_ = response_.json()
        if response_.status_code == 200 and len(catalog_response_['dcat:dataset']) >= 1:
            first_offer_ = catalog_response_['dcat:dataset']
            print(
                f"Offer with type {first_offer_['type']} already exists. Skipping creation.")
        else:
            payload_ = create_edc_registry_asset_payload(aas_url_, registry_asset_id_)
            response_ = session_.request(method="POST", url=asset_url_,
                                         headers=header_,
                                         data=payload_)
            print(response_)
            if response_.status_code > 205:
                print(response_.text)
            else:
                print(f"Successfully created registry asset {response_.json()['@id']}.")

            print("Create registry edc contract definition")
            payload_ = create_edc_contract_definition_payload(policy_, registry_asset_id_)
            response_ = session_.request(method="POST", url=edc_upload_url_ + edc_contract_definition_path_,
                                         headers=header_,
                                         data=payload_)
            print_response(response_)


def search_for_asset_in_catalog(edc_catalog_path_, edc_upload_url_, edc_url_, headers_, session_, asset_id_):
    catalog_url_ = edc_upload_url_ + edc_catalog_path_
    payload_ = {
        "@context": edc_context(),
        "edc:protocol": "dataspace-protocol-http",
        "edc:providerUrl": f"{edc_url_}",
        "edc:querySpec": {
            "edc:filterExpression": {
                "@type": "edc:Criterion",
                "edc:operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
                "edc:operator": "=",
                "edc:operandRight": f"{asset_id_}"
            }
        }
    }
    print(f"Query Catalog for notification assets {catalog_url_}")
    return session_.request(method="POST", url=catalog_url_, headers=headers_, data=json.dumps(payload_))


if __name__ == "__main__":
    timestamp_start = time.time()
    parser = argparse.ArgumentParser(description="Script to upload testdata into CX-Network.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", type=str, help="Test data file location", required=True)
    parser.add_argument("-s", "--submodel", type=str, nargs="*", help="Submodel server display URLs", required=True)
    parser.add_argument("-su", "--submodelupload", type=str, nargs="*", help="Submodel server upload URLs",
                        required=False)
    parser.add_argument("-a", "--aas", type=str, help="aas url", required=True)
    parser.add_argument("-au", "--aasupload", type=str, help="aas url", required=False)
    parser.add_argument("-edc", "--edc", type=str, nargs="*", help="EDC provider control plane display URLs",
                        required=True)
    parser.add_argument("--edcBPN", type=str, nargs="*", help="The BPN of the provider EDC", required=True)
    parser.add_argument("-eu", "--edcupload", type=str, nargs="*", help="EDC provider control plane upload URLs",
                        required=False)
    parser.add_argument("-k", "--apikey", type=str, help="EDC provider api key", required=True)
    parser.add_argument("--bpn", help="Faulty BPN which will create a non existing EDC endpoint", required=False)
    parser.add_argument("-p", "--policy", help="Default Policy which should be used for EDC contract definitions",
                        required=False)
    parser.add_argument("-bpns", "--bpns", type=str, nargs="*", help="Filter upload to upload only specific BPNs",
                        required=False)
    parser.add_argument("-d", "--dataplane", type=str, nargs="*", help="EDC provider data plane display URLs",
                        required=False)
    parser.add_argument("--allowedBPNs", type=str, nargs="*",
                        help="The allowed BPNs for digital twin registration in the registry.", required=False)

    args = parser.parse_args()
    config = vars(args)

    filepath = config.get("file")
    submodel_server_urls = config.get("submodel")
    submodel_server_upload_urls = config.get("submodelupload")
    aas_url = config.get("aas")
    aas_upload_url = config.get("aasupload")
    edc_urls = config.get("edc")
    edc_bpns = config.get("edcBPN")
    edc_upload_urls = config.get("edcupload")
    edc_api_key = config.get("apikey")
    bpnl_fail = config.get("bpn")
    default_policy = config.get("policy")
    bpns_list = config.get("bpns")
    dataplane_urls = config.get("dataplane")
    allowedBPNs = config.get("allowedBPNs")

    if dataplane_urls is None:
        raise ArgumentException("Dataplane URLs have to be specified with -d or --dataplane!")

    if submodel_server_upload_urls is None:
        submodel_server_upload_urls = submodel_server_urls
    if edc_upload_urls is None:
        edc_upload_urls = edc_urls

    if default_policy is None:
        default_policy = "default-policy"

    if aas_upload_url is None:
        aas_upload_url = aas_url

    if allowedBPNs is None:
        allowedBPNs = []

    registry_path = "/shell-descriptors"

    check_url_args(submodel_server_upload_urls, submodel_server_urls, edc_upload_urls, edc_urls, dataplane_urls,
                   edc_bpns)

    edc_asset_path = "/management/v3/assets"
    edc_policy_path = "/management/v3/policydefinitions"
    edc_contract_definition_path = "/management/v3/contractdefinitions"
    edc_catalog_path = "/management/v3/catalog/request"
    dataplane_public_path = "/api/public"
    controlplane_public_path = "/api/v1/dsp"

    registry_asset_id = "registry-asset"

    headers = {
        'Content-Type': 'application/json'
    }

    headers_with_api_key = {
        'X-Api-Key': edc_api_key,
        'Content-Type': 'application/json'
    }

    default_policy_definition = {
        "default": {
            "@context": {
                "odrl": "http://www.w3.org/ns/odrl/2/"
            },
            "@id": "default-policy",
            "policy": {
                "@type": "odrl:Set",
                "odrl:permission": []
            }
        }
    }

    # Opening JSON file
    f = open(filepath)
    data = json.load(f)
    f.close()
    testdata = data["https://catenax.io/schema/TestDataContainer/1.0.0"]
    policies = default_policy_definition
    if "policies" in data.keys():
        policies.update(data["policies"])

    contract_number = 1

    retries = Retry(total=5,
                    backoff_factor=0.1)
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    # session.verify = False

    if policies:
        for policy in policies.keys():
            for url in edc_upload_urls:
                create_policy(policies[policy], url, edc_policy_path, headers_with_api_key, session)

    create_registry_asset(edc_upload_urls, edc_bpns, edc_asset_path, edc_contract_definition_path, edc_catalog_path,
                          headers_with_api_key, session, edc_urls, default_policy, registry_asset_id, aas_url)

    edc_asset_ids = []
    for url in dataplane_urls:
        edc_asset_ids.append(uuid.uuid4().urn)
    print(edc_asset_ids)

    for tmp_data in testdata:
        if bpns_list is None or tmp_data["bpnl"] in bpns_list or not bpns_list:
            catenax_id = tmp_data["catenaXId"]
            identification = uuid.uuid4().urn
            tmp_keys = tmp_data.keys()

            specific_asset_ids = []

            submodel_descriptors = []

            name_at_manufacturer = ""
            specific_asset_ids_temp = []
            for tmp_key in tmp_keys:
                if "Batch" in tmp_key or "SerialPart" in tmp_key:
                    specific_asset_ids_temp = copy(tmp_data[tmp_key][0]["localIdentifiers"])
                    name_at_manufacturer = tmp_data[tmp_key][0]["partTypeInformation"]["nameAtManufacturer"].replace(
                        " ",
                        "")
                if "PartAsPlanned" in tmp_key:
                    name_at_manufacturer = tmp_data[tmp_key][0]["partTypeInformation"]["nameAtManufacturer"].replace(
                        " ",
                        "")
                    specific_asset_ids_temp.append({
                        "value": tmp_data[tmp_key][0]["partTypeInformation"]["manufacturerPartId"],
                        "key": "manufacturerPartId"
                    })
            print(name_at_manufacturer)

            manufacturerId = {
                "key": "manufacturerId",
                "value": tmp_data["bpnl"]
            }
            if manufacturerId not in specific_asset_ids_temp:
                specific_asset_ids_temp.append(manufacturerId)

            keys = [{
                "type": "GlobalReference",
                "value": "PUBLIC_READABLE"
            }]
            for bpn in allowedBPNs:
                keys.append({
                    "type": "GlobalReference",
                    "value": bpn
                })
            externalSubjectId = {
                "type": "ExternalReference",
                "keys": keys
            }
            for asset in specific_asset_ids_temp:
                specific_asset_ids.append({
                    "name": asset.get("key"),
                    "value": asset.get("value"),
                    "externalSubjectId": externalSubjectId
                })

            policy_id = default_policy
            if "policy" in tmp_keys:
                policy_id = tmp_data["policy"]
            print(f"Policy: {policy_id}")

            for tmp_key in tmp_keys:
                if "PlainObject" not in tmp_key and "catenaXId" not in tmp_key and "bpn" not in tmp_key \
                        and "policy" not in tmp_key and "urn:bamm:io.catenax.aas:1.0.0#AAS" not in tmp_key:
                    # Prepare submodel endpoint address
                    submodel_url = submodel_server_urls[contract_number % len(submodel_server_urls)]
                    submodel_upload_url = submodel_server_upload_urls[
                        contract_number % len(submodel_server_upload_urls)]
                    edc_url = edc_urls[contract_number % len(edc_urls)]
                    edc_upload_url = edc_upload_urls[contract_number % len(edc_upload_urls)]
                    dataplane_url = dataplane_urls[contract_number % len(dataplane_urls)]
                    edc_asset_id = edc_asset_ids[contract_number % len(edc_asset_ids)]

                    id_short = uuid.uuid4().urn
                    submodel_identification = uuid.uuid4().urn
                    semantic_id = tmp_key

                    endpoint_address = f"{dataplane_url}{dataplane_public_path}/{submodel_identification}"
                    descriptor = create_submodel_descriptor_3_0(id_short, submodel_identification, semantic_id,
                                                                endpoint_address,
                                                                edc_asset_id,
                                                                edc_url)
                    submodel_descriptors.append(json.loads(descriptor))

                    print("Create submodel on submodel server")
                    if tmp_data[tmp_key] != "":
                        payload = create_submodel_payload(tmp_data[tmp_key][0])
                        response = session.request(method="POST",
                                                   url=f"{submodel_upload_url}/{submodel_identification}",
                                                   headers=headers, data=payload)
                        print_response(response)

                    asset_path = edc_upload_url + edc_asset_path
                    print(f"Create edc asset on EDC {asset_path}")
                    payload = create_edc_asset_payload(submodel_url, edc_asset_id)
                    response = session.request(method="POST", url=asset_path, headers=headers_with_api_key,
                                               data=payload)
                    print_response(response)
                    if response.status_code > 205:
                        print("Asset creation failed. Skipping creation of contract definition.")
                    else:
                        print("Create edc contract definition")
                        payload = create_edc_contract_definition_payload(policy_id, edc_asset_id)
                        response = session.request(method="POST", url=edc_upload_url + edc_contract_definition_path,
                                                   headers=headers_with_api_key,
                                                   data=payload)
                        print_response(response)
                    contract_number = contract_number + 1

            if submodel_descriptors:
                print("Create aas shell")
                id_short = uuid.uuid4().urn
                payload = create_aas_shell_3_0(catenax_id, id_short, identification, specific_asset_ids,
                                               submodel_descriptors)
                response = session.request(method="POST", url=f"{aas_upload_url}{registry_path}",
                                           headers=headers,
                                           data=payload)
                print_response(response)

    timestamp_end = time.time()
    duration = timestamp_end - timestamp_start
    print(f"Test data upload completed in {math.ceil(duration)} Seconds")
