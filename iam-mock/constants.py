#
# Copyright (c) 2024 Volkswagen AG
# Copyright (c) 2024 Contributors to the Eclipse Foundation
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
#

from pathlib import Path

"""
Read key information
"""
def read_file(path: Path):
    with path.open() as file:
        file_content = file.read()
    return file_content


# openssl ecparam -name prime256v1 -genkey -out private_key.pem
# openssl ec -in private_key.pem -pubout -out public_key.pem
ES256_PRIVATE_KEY = read_file(Path("keys/private_key.pem"))
ES256_PUBLIC_KEY = read_file(Path("keys/public_key.pem"))

# must be same as used in edc for edc.transfer.proxy.signer.privatekey.alias
EDC_PRIVATE_KEY = read_file(Path("keys/edc.key"))

DID_TRUSTED_ISSUER = "did:web:mock-util-service/trusted-issuer"
DID_CUSTOMER = "did:web:mock-util-service/customer"
DID_SUPPLIER = "did:web:mock-util-service/supplier"
# DID_BPNL00000003AYRE = "did:web:mock-util-service/BPNL00000003AYRE"
# DID_BPNL00000003AZQP = "did:web:mock-util-service/BPNL00000003AZQP"
# DID_BPNL00000003AVTH = "did:web:mock-util-service/BPNL00000003AVTH"
# DID_BPNL00000003AWSS = "did:web:mock-util-service/BPNL00000003AWSS"
# DID_BPNL00000003B0Q0 = "did:web:mock-util-service/BPNL00000003B0Q0"
# DID_BPNS0000000008ZZ = "did:web:mock-util-service/BPNS0000000008ZZ"
# DID_BPNL00000003CNKC = "did:web:mock-util-service/BPNL00000003CNKC"
# DID_BPNL00000003B6LU = "did:web:mock-util-service/BPNL00000003B6LU"
# DID_BPNL00000003CML1 = "did:web:mock-util-service/BPNL00000003CML1"
# DID_BPNS00000008BDFH = "did:web:mock-util-service/BPNS00000008BDFH"
# DID_BPNL00000003B2OM = "did:web:mock-util-service/BPNL00000003B2OM"
# DID_BPNL00000003CSGV = "did:web:mock-util-service/BPNL00000003CSGV"
# DID_BPNL00000003B5MJ = "did:web:mock-util-service/BPNL00000003B5MJ"
# DID_BPNL00000003AXS3 = "did:web:mock-util-service/BPNL00000003AXS3"
# DID_BPNL00000003B3NX = "did:web:mock-util-service/BPNL00000003B3NX"
# DID_BPNL00000000BJTL = "did:web:mock-util-service/BPNL00000000BJTL"

# note: kid_vault = alias used for public key, set in edc.transfer.proxy.token.verifier.publickey.alias
DID_DICT = {
    DID_TRUSTED_ISSUER: {
        "bpnl": "NONE",
        "did_resolve_name": "trusted-issuer",
    },
    DID_SUPPLIER: {
        "bpnl": "BPNL00000003AYRE",
        "did_resolve_name": "supplier",
        "kid_vault": "tokenSignerPublicKey",
        "private_key": EDC_PRIVATE_KEY
    },
    DID_CUSTOMER: {
        "bpnl": "BPNL00000003AZQP",
        "did_resolve_name": "customer",
        "kid_vault": "tokenSignerPublicKey",
        "private_key": EDC_PRIVATE_KEY
    }
}
    # ,
    # DID_BPNL00000003AYRE: {
    #     "bpnl": "BPNL00000003AYRE",
    #     "did_resolve_name": "BPNL00000003AYRE",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003AZQP: {
    #     "bpnl": "BPNL00000003AZQP",
    #     "did_resolve_name": "BPNL00000003AZQP",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003AVTH: {
    #     "bpnl": "BPNL00000003AVTH",
    #     "did_resolve_name": "BPNL00000003AVTH",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # }
    # ,
    # DID_BPNL00000003AWSS: {
    #     "bpnl": "BPNL00000003AWSS",
    #     "did_resolve_name": "BPNL00000003AWSS",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003B0Q0: {
    #     "bpnl": "BPNL00000003B0Q0",
    #     "did_resolve_name": "BPNL00000003B0Q0",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNS0000000008ZZ: {
    #     "bpnl": "BPNS0000000008ZZ",
    #     "did_resolve_name": "BPNS0000000008ZZ",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003CNKC: {
    #     "bpnl": "BPNL00000003CNKC",
    #     "did_resolve_name": "BPNL00000003CNKC",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003B6LU: {
    #     "bpnl": "BPNL00000003B6LU",
    #     "did_resolve_name": "BPNL00000003B6LU",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003CML1: {
    #     "bpnl": "BPNL00000003CML1",
    #     "did_resolve_name": "BPNL00000003CML1",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNS00000008BDFH: {
    #     "bpnl": "BPNS00000008BDFH",
    #     "did_resolve_name": "BPNS00000008BDFH",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003B2OM: {
    #     "bpnl": "BPNL00000003B2OM",
    #     "did_resolve_name": "BPNL00000003B2OM",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003CSGV: {
    #     "bpnl": "BPNL00000003CSGV",
    #     "did_resolve_name": "BPNL00000003CSGV",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003B5MJ: {
    #     "bpnl": "BPNL00000003B5MJ",
    #     "did_resolve_name": "BPNL00000003B5MJ",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003AXS3: {
    #     "bpnl": "BPNL00000003AXS3",
    #     "did_resolve_name": "BPNL00000003AXS3",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # },
    # DID_BPNL00000003B3NX: {
    #     "bpnl": "BPNL00000003B3NX",
    #     "did_resolve_name": "BPNL00000003B3NX",
    #     "kid_vault": "tokenSignerPublicKey",
    #     "private_key": EDC_PRIVATE_KEY,
    # }

"""
lookup did by did_resolve_name
"""
def get_did_for_resolve_name(did_resolve_name: str):
    for key, value in DID_DICT.items():
        if value["did_resolve_name"] == did_resolve_name:
            return key
    return None


"""
lookup did by bpnl
"""
def get_did_for_bpnl(bpnl: str):
    for key, value in DID_DICT.items():
        if value["bpnl"] == bpnl:
            return key
    return None


"""
lookup bpnl by did
"""
def get_bpnl_for_did(did: str):
    entry = DID_DICT.get(did, None)
    return entry["bpnl"] if entry else None
