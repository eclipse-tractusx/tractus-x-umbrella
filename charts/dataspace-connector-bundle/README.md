# Dataspace Connector Bundle

![Version: 1.1.0](https://img.shields.io/badge/Version-1.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) 

Helm chart for Capability Bundle: Dataspace Connector

For more information on the Tractus-X EDC, see https://github.com/eclipse-tractusx/tractusx-edc


**Homepage:** <https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/dataspace-connector-bundle>

### Launching the application

Run this shell command to start the Capability Bundle: Dataspace Connector:

```shell
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm install my-release tractusx-dev/dataspace-connector-bundle
```

For more information to "Bring Your Own" configuration, see the [hausanschluss user guide](/docs/user/guides/hausanschluss-bundles.md#bring-your-own-components).

## Source Code

* <https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/dataspace-connector-bundle>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | postgresql | 15.2.1 |
| https://eclipse-tractusx.github.io/charts/dev | tractusx-connector | 0.11.1 |
| https://helm.releases.hashicorp.com | vault | 0.27.0 |

## Values

### Decentralized Claims Protocol (DCP, formerly IATP) Settings (Bring Your Own)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tractusx-connector.iatp.id | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AZQP"` | Decentralized IDentifier (DID) of the connector |
| tractusx-connector.iatp.trustedIssuers | list | `["did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"]` | Configures the trusted issuers for this runtime |
| tractusx-connector.iatp.sts.dim.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/sts"` | URL where connectors can request SI tokens |
| tractusx-connector.iatp.sts.oauth.token_url | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` | URL where connectors can request OAuth2 access tokens for DIM access |
| tractusx-connector.iatp.sts.oauth.client.id | string | `"BPNL00000003AZQP"` | Client ID for requesting OAuth2 access token for DIM access |
| tractusx-connector.iatp.sts.oauth.client.secret_alias | string | `"client-secret"` | Alias under which the client secret is stored in the vault for requesting OAuth2 access token for DIM access |
| tractusx-connector.participant.id | string | `"BPNL00000003AZQP"` | Business Partner Number (BPN) of the connector |
| tractusx-connector.controlplane.env | map | `{"TX_IAM_IATP_CREDENTIALSERVICE_URL":"http://ssi-dim-wallet-stub.tx.test/api"}` | Extra environment variables that will be pass onto deployment pods |
| tractusx-connector.controlplane.bdrs.server.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/v1/directory"` | URL of the BPN/DID Resolution Service |
| tractusx-connector.dataplane.env | map | `{"TX_IAM_IATP_CREDENTIALSERVICE_URL":"http://ssi-dim-wallet-stub.tx.test/api"}` | Extra environment variables that will be pass onto deployment pods |

### EDC Installation Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tractusx-connector.controlplane.endpoints.management.authKey | string | `"TEST1"` | Authentication key. Must be attached to each request as `X-Api-Key` header |
| tractusx-connector.dataplane.token.signer.privatekey_alias | string | `"tokenSignerPrivateKey"` | Alias under which the private key (JWK or PEM format) is stored in the vault |
| tractusx-connector.dataplane.token.verifier.publickey_alias | string | `"tokenSignerPublicKey"` | Alias under which the public key (JWK or PEM format) is stored in the vault, that belongs to the private key which was referred to at `dataplane.token.signer.privatekey_alias` |

### EDC Ingress Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tractusx-connector.controlplane.ingresses[0].enabled | bool | `true` | Enables ingress creation |
| tractusx-connector.controlplane.ingresses[0].hostname | string | `"example-controlplane.tx.test"` | The hostname to be used to precisely map incoming traffic onto the underlying network service |
| tractusx-connector.controlplane.ingresses[0].endpoints | list | `["default","protocol","management"]` | EDC endpoints exposed by this ingress resource |
| tractusx-connector.controlplane.ingresses[0].tls.enabled | bool | `false` | Enables TLS on the ingress resource |
| tractusx-connector.dataplane.ingresses[0].enabled | bool | `true` | Enables ingress creation |
| tractusx-connector.dataplane.ingresses[0].hostname | string | `"example-dataplane.tx.test"` | The hostname to be used to precisely map incoming traffic onto the underlying network service |
| tractusx-connector.dataplane.ingresses[0].endpoints | list | `["default","public"]` | EDC endpoints exposed by this ingress resource |
| tractusx-connector.dataplane.ingresses[0].tls.enabled | bool | `false` | Enables TLS on the ingress resource |

### EDC PostgreSQL Options (Bring Your Own)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tractusx-connector.postgresql.jdbcUrl | string | `"jdbc:postgresql://{{ .Release.Name }}-postgresql:5432/edc"` | JDBC connection URL for PostgreSQL |
| tractusx-connector.postgresql.auth.database | string | `"edc"` | Database name |
| tractusx-connector.postgresql.auth.username | string | `"user"` | Database username |
| tractusx-connector.postgresql.auth.password | string | `"password"` | Database password |

### EDC Vault Options (Bring Your Own)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| tractusx-connector.vault.hashicorp.url | string | `"http://{{ .Release.Name }}-vault:8200"` | URL for HashiCorp Vault |
| tractusx-connector.vault.hashicorp.token | string | `"root"` | Root token for Vault authentication |
| tractusx-connector.vault.hashicorp.paths.secret | string | `"/v1/secret"` | Base path for secrets in Vault |
| tractusx-connector.vault.hashicorp.paths.folder | string | `""` | Subfolder for secrets |

### PostgreSQL Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| postgresql.enabled | bool | `true` | Enable embedded PostgreSQL deployment |
| postgresql.auth.database | string | `"edc"` | Database name |
| postgresql.auth.username | string | `"user"` | Database username |
| postgresql.auth.password | string | `"password"` | Database password |
| postgresql.primary.persistence.enabled | bool | `false` | Enable persistent storage for PostgreSQL |
| postgresql.primary.persistence.size | string | `"10Gi"` | Size of persistent volume |

### Vault Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| vault.enabled | bool | `true` | Enable embedded HashiCorp Vault deployment |
| vault.server.standalone.enabled | bool | `true` | Enable standalone mode for Vault |
| vault.server.dev.enabled | bool | `true` | Enable development mode for Vault |
| vault.server.dev.devRootToken | string | `"root"` | Root token for dev mode |

## Contributing

Contributions are welcome! Please see our [Contributing Guide](/CONTRIBUTING.md) for details.

----------------------------------------------
Autogenerated from chart metadata using [helm-docs](https://github.com/norwoodj/helm-docs/)  
Generate this document by running `helm-docs -s file` in this folder
