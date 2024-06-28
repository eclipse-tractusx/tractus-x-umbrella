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

from jwtUtils import create_token_from_payload, decode_token, create_jwt_from_claims
from constants import DID_TRUSTED_ISSUER, get_did_for_bpnl, DID_DICT


"""
embeds a VC in a JWT for the given information (mainly scope = vc)

Differentiates self-IATP and vc for external partner
"""
def create_jwt_vc(did_issuer: str, did_subject: str, did_audience: str, bpnl_subject: str, scope: str):

    self_iatp_flag = did_subject == did_audience
    payload = {
        "iss": did_issuer,
        "sub": did_issuer, # TODO: why no subject?
        "aud": did_audience, #TODO: audience needed? Seems like not as this credential is pulled on behalf of the subject / RP
        "nbf": 1541493724,
        "iat": 1541493724,
        "exp": 32481718133,
        "vc": create_verifiable_credential(did_issuer=did_issuer, did_subject=did_subject, bpnl_subject=bpnl_subject, scope=scope),
    }

    return create_token_from_payload(payload, did_issuer)


"""
creates a plain VC (no jwt) for a given scope
"""
def create_verifiable_credential(did_issuer: str, did_subject: str, bpnl_subject: str, scope: str):

    needs_version = False if scope.startswith("Membership") else True

    print(f"Create VC for scope {scope}")
    vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://w3id.org/security/suites/jws-2020/v1",
            "https://w3id.org/catenax/credentials",
            "https://w3id.org/vc/status-list/2021/v1"
        ],
        "id": "some-identifier",
        "issuer": did_issuer,
        "issuanceDate": "2021-06-16T18:56:59Z",
        # "expirationDate": "2199-12-31T23:59:59Z", #seems to be only set if checked
        "type": [
            "VerifiableCredential",
            scope
        ],
        "credentialSubject": {
            "id": did_subject,
            "holderIdentifier": bpnl_subject
        },
    }

    if needs_version:
        vc["credentialSubject"]["contractVersion"] = "1.0"
    return vc


"""
creates a vp with n vcs where n = amount of scopes

Note: only MembershipCredential and FrameworkAgreements in version 1.0 are supported
"""
def create_verifiable_presentation(did_subject: str, did_issuer: str, did_audience: str, scopes: [str] = ["MembershipCredential"]):

    bpnl = DID_DICT[did_subject]["bpnl"]
    # Create a VC per scope
    vcs = [create_jwt_vc(DID_TRUSTED_ISSUER, did_subject, did_audience, bpnl, scope) for scope in scopes]

    claims = {
        "iss": did_issuer,
        "sub": did_subject,
        "aud": did_audience, # todo check
        "nbf": 1541493724,
        "iat": 1541493724,
        "exp": 32481718133,
        "vp": {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://www.w3.org/2018/credentials/examples/v1"
            ],
            "type": [
                "VerifiablePresentation",
                "CredentialManagerPresentation"
            ],
            "verifiableCredential": vcs
        }
    }

    return create_token_from_payload(claims, did_issuer)
