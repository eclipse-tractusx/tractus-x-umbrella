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

import jwt
from constants import ES256_PRIVATE_KEY, DID_DICT


"""
creates a jwt adding time information (nbf, iat, exp) to jwt

claims: expects participant information (iss, aud, sub) to be present
issuer: to sign the jwt
scope: scope needed that will be added to the claims as "scope" and embeds the payload as jwt in "token"
embed_token: put a representation of this token as "token" claim into the token
"""
def create_jwt_from_claims(claims: dict, issuer: str, scope: str = None, embed_token: bool = False) -> dict:

    base_claims = {
        "iat": 1541493724,
        "exp": 32481718133,
    }
    claims.update(base_claims)

    # TODO check for update
    if scope: # GRANT ACCESS request includes scope and token representation
        claims["scope"] = scope
        claims["token"] = create_token_from_payload(claims, issuer)
    elif embed_token: # refresh token needs access token representation
        claims["token"] = create_token_from_payload_with_vault_key(claims, issuer, DID_DICT[issuer]["kid_vault"], DID_DICT[issuer]["private_key"])
    else:
        print("No scope given for self-issued token. No token claim created for it.")

    print(f"Created jwt for payload {claims} signed by {issuer}")

    return create_token_from_payload(claims, issuer)


"""
create a jwt for the payload, signed by did_signer using information from the vault (preconfigured information)

Creates a header with a kid for a key, that can be understood by LocalPublicKeyServiceImpl
https://github.com/eclipse-edc/Connector/blob/main/core/common/lib/keys-lib/src/main/java/org/eclipse/edc/keys/LocalPublicKeyServiceImpl.java#L44
"""
def create_token_from_payload_with_vault_key(payload: str, did_signer: str, kid: str, private_key: str):

    header = {
        "alg": "RS256",
        "kid": kid
    }

    jwt_token = jwt.encode(payload, private_key, algorithm='RS256', headers=header)

    return jwt_token


"""
create a jwt for the payload, signed by did_signer

Creates a header with a kid that can be handeled by the did exposed by mock_util.py
"""
def create_token_from_payload(payload: str, did_signer: str):

    header = {
        "alg": "ES256",
        "typ": "JWT",
        "kid": did_signer+"#key1"
    }

    jwt_token = jwt.encode(payload, ES256_PRIVATE_KEY, algorithm='ES256', headers=header)

    return jwt_token


"""
decode token without signature check (NON-PRODUCTION, MOCK!)
"""
def decode_token(jwt_token: str):
    # don't check signature
    return jwt.decode(jwt_token, options={"verify_signature": False})
