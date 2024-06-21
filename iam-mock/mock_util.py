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

import socket
from cryptography.hazmat.backends import default_backend
from fastapi import FastAPI, Request
import logging
import base64
from cryptography.hazmat.primitives import serialization
from jwtUtils import decode_token, create_jwt_from_claims
from constants import ES256_PUBLIC_KEY, DID_TRUSTED_ISSUER, get_did_for_resolve_name, get_did_for_bpnl
from credential_service import create_verifiable_presentation
import uuid
from pathlib import Path


cwd = Path(".")
print(cwd.cwd())
print([path.name for path in cwd.iterdir()])

app = FastAPI()

logger = logging.getLogger("fastapi")

"""
store STS GRANT ACCESS Request JWT token for uuid.

Uuid is inserted into token as 'token_id' to use the token in SIGN TOKEN Request (remember request granted)
"""
id_token_map = {}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/edr-log")
async def log(request: Request):
    hostname = socket.gethostbyaddr(request.client.host)[0]
    print("CALLED /edr-log from ", hostname)
    body = await request.json()

    # Log the data
    print(body)

    return {"message": "Data logged successfully"}


"""
Returns self-issued credential token following the dim adjustments

Follows more or less the DIM Dispatcher mock
see https://github.com/eclipse-tractusx/tractusx-edc/blob/d7d3586ffc4ef03c858e38fde6bfa8687efa50c9/edc-tests/edc-controlplane/iatp-tests/src/test/java/org/eclipse/tractusx/edc/tests/transfer/iatp/dispatchers/DimDispatcher.java
"""
@app.post("/sts")
async def secure_token_service(request: Request):

    print("")
    body = await request.json()
    sign_token_flag = True if body.get("grantAccess", None) is None else False
    hostname = socket.gethostbyaddr(request.client.host)[0]
    print("CALLED sts /sts for ", "SIGN TOKEN REQUEST" if sign_token_flag else "GRANT ACCESS REQUEST", " from ", hostname)

    print("POST with body ", body)
    print("bearer of requestor is set as auth header" if request.headers["authorization"] else "bearer of requestor is NOT set as auth header")
    print(f"bearer: {request.headers['authorization']}")
    print(f"Request params received: {request.query_params}")

    # handle body similar to https://github.com/eclipse-tractusx/tractusx-edc/blob/d7d3586ffc4ef03c858e38fde6bfa8687efa50c9/edc-tests/edc-controlplane/iatp-tests/src/test/java/org/eclipse/tractusx/edc/tests/transfer/iatp/dispatchers/DimDispatcher.java
    grant_access = body.get("grantAccess", None)
    if sign_token_flag:
        sign_token = body["signToken"]

        decoded_token = decode_token(sign_token["token"])

        # try to lookup existing token, if found use it
        # else we're in token refresh
        token_id = decoded_token.get('token_id', None)
        if token_id:
            token = id_token_map[token_id]
            decoded_token = decode_token(token)
            print(f"Identified matching token (decoded) {decoded_token}")
            id_token_map.pop(token_id)

            # common request: issued by trusted issuer
            claims = {
                "iss": decoded_token["iss"],
                "sub": decoded_token["sub"],
                "aud": decoded_token["aud"]
            }

            print(f"Request contains issuer {claims['iss']}, subject {claims['sub']}, audience {claims['aud']}, token {token}")
            token = create_jwt_from_claims(claims, sign_token["issuer"], None)
            print(f"Created jwt token: {token}")
            vp = token

        else:
            # refresh token request: iss, sub = client did
            claims = {
                "iss": get_did_for_bpnl(decoded_token["aud"]),
                "sub": get_did_for_bpnl(decoded_token["aud"]),
                "aud": get_did_for_bpnl(decoded_token["sub"]),
                "jti": decoded_token["jti"],
                "iat": decoded_token["iat"],
                "exp": decoded_token["exp"],
            }

            print(f"Request contains issuer {claims['iss']}, subject {claims['sub']}, audience {claims['aud']}, token {decoded_token}")
            token = create_jwt_from_claims(claims, claims["iss"], None, True)
            print(f"Created jwt token: {token}")
            vp = token

    else:
        token_id = str(uuid.uuid4())

        claims = {
            "iss": grant_access["consumerDid"],
            "sub": grant_access["consumerDid"],
            "aud": grant_access["providerDid"],
            "token_id": token_id
        }

        print(f"Request issuer {claims['iss']}, subject {claims['sub']}, audience {claims['aud']}")
        print(f"Message contains bearer from {claims['iss']} oAuth Service")
        scope = " ".join(grant_access["credentialTypes"]) if grant_access["credentialTypes"] is not None else None

        token = create_jwt_from_claims(claims, grant_access["consumerDid"], scope)
        id_token_map[token_id] = token
        vp = token

    return {"jwt": vp}


"""
provides the VP as soon as the connector asks for it.

Creates a PresentationResponseMessage with a VP following this structure:
JWT enapsulating VP
  vp:
    {
      ...
      verifiableCredential: [
        vc jwt for scope 1,
        vc jwt for scope 2
      ]
    }
}
"""
@app.post("/presentations/query")
async def query_presentation(request: Request):

    print("")
    hostname = socket.gethostbyaddr(request.client.host)[0]
    print("CALLED /presentations/query from ", hostname)

    # consider subject to be holder & audience
    jwt_requestor = extract_jwt_from_headers(request.headers)

    body = await request.json()
    print("POST with body ", body)
    print("JWT for query_presentation ", jwt_requestor)
    print(f"Query for issuer {jwt_requestor['iss']}, sub {jwt_requestor['sub']}, audience {jwt_requestor['aud']} with scope {jwt_requestor.get('scope', '*no value set for scope*')}")
    print("Request contains header for the issuer's oauth2 system")

    cx_scopes = [scope[1] for scope in extract_scopes(body["scope"])]
    print(f"Will try to Mock CX Credential Scopes {cx_scopes}")

    response = {
      "@context": [
        "https://w3id.org/tractusx-trust/v0.8"
      ],
      "@type": "PresentationResponseMessage",
      "presentation": [create_verifiable_presentation(jwt_requestor['sub'], jwt_requestor['iss'], jwt_requestor['aud'], cx_scopes)],
    }

    print("Response: ", response)

    return response


def get_bearer_from_headers(headers: [str]):
    return headers["authorization"][len("Bearer "):]


def extract_jwt_from_headers(headers: [str]):
    return decode_token(get_bearer_from_headers(headers))


"""
Returns a DID document for the specified partner

Mock: 
- all DIDs use the same key pair for signing
- Credential Service is needed as fallback
"""
@app.get("/{partner_did}/{did_path:path}")
def return_did(request: Request, partner_did: str, did_path: str):

    print("")
    hostname = socket.gethostbyaddr(request.client.host)[0]
    print(f"CALLED /{partner_did}/{did_path} from ", hostname)

    # get DID constant for path used
    did_id = get_did_for_resolve_name(partner_did)

    # put elyptic curves accordingly
    public_key = serialization.load_pem_public_key(ES256_PUBLIC_KEY.encode(), backend=default_backend())
    public_key_numbers = public_key.public_numbers()

    x = base64.urlsafe_b64encode(public_key_numbers.x.to_bytes(32, 'big')).rstrip(b'=').decode()
    y = base64.urlsafe_b64encode(public_key_numbers.y.to_bytes(32, 'big')).rstrip(b'=').decode()

    did_to_return = {
      "service": [
          {
              "id": did_id,
              "type": "CredentialService",
              "serviceEndpoint": "http://mock-util-service:80"
          }
      ],
      "verificationMethod": [
        {
          "id": did_id + "#key1",  # like "did:web:nginx:bdrs-client#key-1"
          "type": "JsonWebKey2020",
          "controller": did_id,
          "publicKeyJwk": {
            "kty": "EC",
            "crv": "P-256",
            "kid": did_id + "#key1",  # like "did:web:nginx:bdrs-client#key-1"
            "x": x,
            "y": y
          }
        }
      ],
      "authentication": [],
      "id": "http://tx-test.com/7bffc00d-3142-4cf2-a858-57c7493577f1",
      "@context": [
        "https://w3id.org/did-resolution/v1"
      ]
    }

    print("RETURN DID: ", did_to_return)

    return did_to_return


"""
returns list of tuples in format (namespace: str, credential: str, access: str)
"""
def extract_scopes(scopes: [str]):
    return [tuple(scope.split(":")) for scope in scopes]
