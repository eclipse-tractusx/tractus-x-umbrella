Basically, there are two types of IATP flows used by the connector in Catena-X Data Spaces:

- Self IATP (e.g. get MembershipCredential for BDRS)
- IATP (e.g. used for catalog request, see simplified in `./credential_requests.puml`)

See [README.md](../README.md) for the different capabilities

This document mainly gives some learnings regarding
the [Tractus-X Verifiable Presentation flow](https://github.com/eclipse-tractusx/identity-trust/blob/main/specifications/verifiable.presentation.protocol.md)

# Resolving DIDs

Triggered via `bdrs` client of a party when `catalog` call is invoked to

- identify DID for Partner in Access Policy
- identify DID for Partner for Contract Policies (e.g. Membership)

Additionally, DIDs may be resolved

- verify identities during data space protocol communication.
- to determine the Credential Service Endpoint who is responsible for a partner

# Self-issued token

A participant may create a self-issued token that can be used to request VPs at the credential service.
The token follows this spec https://datatracker.ietf.org/doc/html/rfc9068

The relying party verifies the token https://openid.net/specs/openid-connect-self-issued-v2-1_0.html#section-11.1
The relying party may query additional information from the cs using token

- get did via `sub` claim
- resolve did
- extract `CredentialService` from `service` from did
- query for presentation

Note: If a `bearer_access_scope` is given, this is added as a `token` claim so that a relying party can authenticate on
behalf of the holder at the credential service to get the VP for scopes in question.

See more details for STS flow in  https://openid.net/specs/openid-connect-self-issued-v2-1_0.html#section-1.1

## Special case for EDR token refresh

docs: https://github.com/eclipse-tractusx/tractusx-profiles/blob/main/tx/refresh/refresh.token.grant.profile.md

EDR use the local keys provided via edc config. When mocking the edr refresh, these private keys need to be used to sign
the jwt. Also, the kid in the jwt header needs to be the alias in vault. Both is hard coded in constants and
`generate-keys.sh`.

EDR information are stored in the vault

- `edr-{transfer-proccess-id}` = information returned from `edr/{transfer-process-id}/dataadress`
- `jti` = the internal id of the EDR token. It's also stored in the respective db (see data plane plugins) -> you can
  still use one vault for several edc in testing

Relevant for EDR content:

- `iat` = now
- `exp` = now + seconds configured for refresh in provider data plane
- `jti` = see above
- `iss` = `aud` = consumer
- `sub` = provider

# Credential Service calls

This is the real wallet allowing to store issued credentials and create verifiable presentations to proof the ownership
of a verifiable credential

## Issue credential / Store credential

Ignored in Mock. We always do a pass all. Normally some trusted issuer would hand over the credentials into a wallet.

## Query for presentation

In Tractus-X Data Spaces with DIM (what this service mocks) the query is done on behalf of the holder.

One needs an access token for that an the relying party may get a vp as previously granted via the STS.
