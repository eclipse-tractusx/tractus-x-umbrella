# Connected Services

This document provides detailed information about how various Tractus-X services integrate with the External Secrets
Operator and utilize secrets from HashiCorp Vault.

## Overview

The Tractus-X Umbrella includes numerous services that require secure access to sensitive information such as:

- Database credentials
- API keys and tokens
- Client secrets for OAuth/OIDC
- Encryption keys
- Service account credentials
- TLS certificates

Each service is configured to use external secrets through the External Secrets Operator, providing centralized secret
management and enhanced security.

## Identity and Access Management Services

### CentralIDP (Keycloak)

CentralIDP serves as the central identity provider for the Tractus-X ecosystem.

#### Required Secrets

| Secret Name                                  | Purpose                     | Keys                                            |
|----------------------------------------------|-----------------------------|-------------------------------------------------|
| `umbrella-centralidp`                        | Keycloak admin credentials  | `admin-password`                                |
| `umbrella-centralidp-postgresql`             | Database credentials        | `postgres-password`, `password`                 |
| `umbrella-centralidp-clients`                | OAuth client secrets        | `miw`, `bpdm`, `bpdm-gate`, `bpdm-orchestrator` |
| `umbrella-centralidp-base-service-accounts`  | Service account credentials | Multiple service account secrets                |
| `umbrella-centralidp-extra-service-accounts` | Additional service accounts | Test service account credentials                |

#### Configuration Example

```yaml
centralidp:
  keycloak:
    auth:
      # Admin password from external secret
      existingSecret: "umbrella-centralidp"
    postgresql:
      auth:
        # Database credentials from external secret
        existingSecret: "umbrella-centralidp-postgresql"

  realmSeeding:
    clients:
      # OAuth client secrets
      existingSecret: "umbrella-centralidp-clients"
    serviceAccounts:
      # Base service account credentials
      existingSecret: "umbrella-centralidp-base-service-accounts"
    extraServiceAccounts:
      # Additional service account credentials
      existingSecret: "umbrella-centralidp-extra-service-accounts"
```

#### Vault Secret Structure

```bash
# Admin credentials
vault kv put secret/umbrella-centralidp \
  admin-password="secure-admin-password"

# Database credentials
vault kv put secret/umbrella-centralidp-postgresql \
  postgres-password="secure-db-password" \
  password="secure-db-password"

# Client secrets
vault kv put secret/umbrella-centralidp-clients \
  miw="client-secret-miw" \
  bpdm="client-secret-bpdm" \
  bpdm-gate="client-secret-bpdm-gate" \
  bpdm-orchestrator="client-secret-bpdm-orchestrator"
```

### SharedIDP (Keycloak)

SharedIDP provides shared identity services across multiple tenants.

#### Required Secrets

| Secret Name                                    | Purpose                    | Keys                            |
|------------------------------------------------|----------------------------|---------------------------------|
| `umbrella-sharedidp`                           | Keycloak admin credentials | `admin-password`                |
| `umbrella-sharedidp-postgresql`                | Database credentials       | `postgres-password`, `password` |
| `umbrella-sharedidp-cx-operator-realm-seeding` | Realm configuration        | User and mailing configuration  |
| `umbrella-sharedidp-master-realm-seeding`      | Master realm clients       | Service account credentials     |

#### Configuration Example

```yaml
sharedidp:
  keycloak:
    auth:
      existingSecret: "umbrella-sharedidp"
    postgresql:
      auth:
        existingSecret: "umbrella-sharedidp-postgresql"

  realmSeeding:
    realms:
      cxOperator:
        existingSecret: "umbrella-sharedidp-cx-operator-realm-seeding"
      master:
        existingSecret: "umbrella-sharedidp-master-realm-seeding"
```

## Data Exchange Services

### Data Consumer Services

Data consumers require database credentials and connector configuration.

#### DataConsumer One

```yaml
dataconsumerOne:
  dataspace-connector-bundle:
    tractusx-connector:
      controlplane:
        envValueFrom:
          EDC_DATASOURCE_DEFAULT_PASSWORD:
            secretKeyRef:
              name: umbrella-dataconsumer-1-db
              key: password
      dataplane:
        envValueFrom:
          EDC_DATASOURCE_DEFAULT_PASSWORD:
            secretKeyRef:
              name: umbrella-dataconsumer-1-db
              key: password
      postgresql:
        auth:
          existingSecret: umbrella-dataconsumer-1-db
```

#### Required Secrets

| Secret Name                  | Purpose              | Keys                            |
|------------------------------|----------------------|---------------------------------|
| `umbrella-dataconsumer-1-db` | Database credentials | `postgres-password`, `password` |
| `umbrella-dataconsumer-2-db` | Database credentials | `postgres-password`, `password` |

### TX Data Provider

The data provider service requires database and registry credentials.

#### Configuration Example

```yaml
tx-data-provider:
  dataspace-connector-bundle:
    tractusx-connector:
      controlplane:
        envValueFrom:
          EDC_DATASOURCE_DEFAULT_PASSWORD:
            secretKeyRef:
              name: umbrella-dataprovider-db
              key: password
      postgresql:
        auth:
          existingSecret: umbrella-dataprovider-db

  digital-twin-bundle:
    digital-twin-registry:
      postgresql:
        auth:
          existingSecret: external-dataprovider-dtr-db
```

#### Required Secrets

| Secret Name                    | Purpose                | Keys                            |
|--------------------------------|------------------------|---------------------------------|
| `umbrella-dataprovider-db`     | Connector database     | `postgres-password`, `password` |
| `external-dataprovider-dtr-db` | Registry database      | `postgres-password`, `password` |
| `umbrella-dataprovider-dtr`    | Registry configuration | Multiple configuration keys     |

## Portal Services

### Portal Backend

The portal backend requires multiple secrets for different integrations.

#### Configuration Example

```yaml
portal:
  backend:
    keycloak:
      # Keycloak integration secrets
      secret: "portal-backend-keycloak"
    mailing:
      # Mailing service secrets
      secret: "portal-backend-mailing"
    interfaces:
      # External service integration secrets
      secret: "portal-backend-interfaces"
  postgresql:
    auth:
      # Database credentials
      existingSecret: "portal-postgres"
```

#### Required Secrets

| Secret Name                 | Purpose              | Keys                                            |
|-----------------------------|----------------------|-------------------------------------------------|
| `portal-backend-keycloak`   | Keycloak integration | `central-client-secret`, `shared-client-secret` |
| `portal-backend-mailing`    | Email configuration  | `password`, `provisioning-sharedrealm-password` |
| `portal-backend-interfaces` | External APIs        | Multiple client secrets and encryption keys     |
| `portal-postgres`           | Database credentials | `postgres-password`, `portal-password`, etc.    |

#### Vault Secret Examples

```bash
# Keycloak integration
vault kv put secret/portal-backend-keycloak \
  central-client-secret="central-secret" \
  shared-client-secret="shared-secret"

# Mailing configuration
vault kv put secret/portal-backend-mailing \
  password="smtp-password" \
  provisioning-sharedrealm-password="realm-password"

# External interfaces
vault kv put secret/portal-backend-interfaces \
  bpdm-client-secret="bpdm-secret" \
  custodian-client-secret="custodian-secret" \
  clearinghouse-client-secret-default="clearinghouse-secret"
```

## Business Partner Data Management (BPDM)

### BPDM Services

BPDM services require database credentials and inter-service communication secrets.

#### Configuration Example

```yaml
# BPDM Gate
bpdm-gate:
  postgresql:
    auth:
      existingSecret: "bpdm-postgres"

  # External secrets for service configuration
  externalSecrets:
    enabled: true
    secretName: "umbrella-bpdm-gate"

# BPDM Pool
bpdm-pool:
  postgresql:
    auth:
      existingSecret: "bpdm-postgres"

  externalSecrets:
    enabled: true
    secretName: "umbrella-bpdm-pool"
```

#### Required Secrets

| Secret Name                  | Purpose             | Keys                                 |
|------------------------------|---------------------|--------------------------------------|
| `bpdm-postgres`              | Shared database     | `postgres-password`, `password`      |
| `umbrella-bpdm-gate`         | Gate service config | Client secrets and database password |
| `umbrella-bpdm-pool`         | Pool service config | Client secrets and database password |
| `umbrella-bpdm-orchestrator` | Orchestrator config | Database password                    |

## SSI and Credential Services

### SSI Credential Issuer

The SSI Credential Issuer requires portal and wallet integration secrets.

#### Configuration Example

```yaml
ssi-credential-issuer:
  existingSecret: external-ssi-credential-issuer
  postgresql:
    auth:
      existingSecret: "{{ .Release.Name }}-issuer-postgres"
```

#### Required Secrets

| Secret Name                      | Purpose              | Keys                                                            |
|----------------------------------|----------------------|-----------------------------------------------------------------|
| `external-ssi-credential-issuer` | Service integration  | `portal-client-secret`, `wallet-client-secret`, encryption keys |
| `umbrella-issuer-postgres`       | Database credentials | `postgres-password`, `password`                                 |

### SSI DIM Wallet Stub

#### Configuration Example

```yaml
identity-and-trust-bundle:
  ssi-dim-wallet-stub:
    wallet:
      secretName: external-ssi-dim-wallet-secret
```

#### Required Secrets

| Secret Name                      | Purpose            | Keys                                       |
|----------------------------------|--------------------|--------------------------------------------|
| `external-ssi-dim-wallet-secret` | Wallet integration | `PORTAL_CLIENT_SECRET`, `PORTAL_CLIENT_ID` |

## Discovery Services

### BPN Discovery

BPN Discovery service requires database and OAuth configuration.

#### Configuration Example

```yaml
bpndiscovery:
  postgresql:
    auth:
      existingSecret: "secret-bpndiscovery-postgres-init"
```

#### Required Secrets

| Secret Name                         | Purpose               | Keys                                          |
|-------------------------------------|-----------------------|-----------------------------------------------|
| `secret-bpndiscovery-postgres-init` | Database and config   | Database credentials and Spring configuration |
| `external-bpndiscovery`             | Service configuration | OAuth and discovery configuration             |

### Discovery Finder

#### Configuration Example

```yaml
discoveryfinder:
  postgresql:
    auth:
      existingSecret: secret-discoveryfinder-postgres-init
```

#### Required Secrets

| Secret Name                            | Purpose               | Keys                                           |
|----------------------------------------|-----------------------|------------------------------------------------|
| `secret-discoveryfinder-postgres-init` | Database credentials  | `postgres-password`, `password`, Spring config |
| `umbrella-discoveryfinder`             | Service configuration | OAuth and discovery settings                   |

## Administrative Services

### PgAdmin4

Database administration interface.

#### Configuration Example

```yaml
pgadmin4:
  existingSecret: "external-pgadmin4"
```

#### Required Secrets

| Secret Name         | Purpose           | Keys       |
|---------------------|-------------------|------------|
| `external-pgadmin4` | Admin credentials | `password` |

## Service-Specific Integration Patterns

### Environment Variable Injection

Many services use environment variables for secret injection:

```yaml
service:
  envValueFrom:
    DATABASE_PASSWORD:
      secretKeyRef:
        name: service-database-secret
        key: password
    API_KEY:
      secretKeyRef:
        name: service-api-secret
        key: api-key
```

### Existing Secret References

Services reference pre-created secrets:

```yaml
service:
  auth:
    existingSecret: "service-auth-secret"
  database:
    auth:
      existingSecret: "service-db-secret"
```

### Volume Mounts

Some services mount secrets as files:

```yaml
service:
  volumes:
    - name: secret-volume
      secret:
        secretName: service-file-secret
  volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
```

## Secret Naming Conventions

### Standard Patterns

- **Database secrets**: `{service}-{database}-{type}`
    - Example: `umbrella-centralidp-postgresql`
- **Service secrets**: `{service}-{purpose}`
    - Example: `portal-backend-keycloak`
- **External secrets**: `external-{service}`
    - Example: `external-pgadmin4`

### Key Naming

- **Database passwords**: `password`, `postgres-password`
- **Admin credentials**: `admin-password`, `admin-username`
- **Client secrets**: `{client-name}-client-secret`
- **API keys**: `api-key`, `{service}-api-key`

## Troubleshooting Service Integration

### Common Issues

1. **Secret Not Found**
   ```bash
   kubectl get secrets -n umbrella | grep service-name
   kubectl describe externalsecret service-secret -n umbrella
   ```

2. **Wrong Secret Key**
   ```bash
   kubectl get secret service-secret -o yaml
   kubectl describe pod service-pod | grep -A 10 "Environment"
   ```

3. **Permission Issues**
   ```bash
   kubectl logs deployment/external-secrets -n external-secrets-system
   kubectl describe secretstore vault-store -n umbrella
   ```

### Validation Commands

```bash
# Check if secret exists
kubectl get secret umbrella-centralidp -n umbrella

# Verify secret content (base64 encoded)
kubectl get secret umbrella-centralidp -o jsonpath='{.data.admin-password}' | base64 -d

# Check ExternalSecret status
kubectl get externalsecret umbrella-centralidp -n umbrella
kubectl describe externalsecret umbrella-centralidp -n umbrella

# Verify service is using the secret
kubectl describe deployment centralidp-keycloak -n umbrella
```

## Security Best Practices

### Service-Specific Recommendations

1. **Use dedicated secrets per service**
2. **Implement least-privilege access**
3. **Regular secret rotation**
4. **Monitor secret access**
5. **Use service-specific Vault policies**

### Example Vault Policy for CentralIDP

```hcl
# centralidp-policy.hcl
path "secret/data/umbrella-centralidp*" {
  capabilities = ["read"]
}

path "secret/metadata/umbrella-centralidp*" {
  capabilities = ["list"]
}
```

## Migration Guide

### From Hardcoded Secrets to External Secrets

1. **Identify current secrets**:
   ```bash
   kubectl get secrets -n umbrella
   ```

2. **Create Vault secrets**:
   ```bash
   vault kv put secret/service-name key=value
   ```

3. **Update service configuration**:
   ```yaml
   service:
     auth:
       existingSecret: "service-name"
   ```

4. **Deploy and verify**:
   ```bash
   helm upgrade umbrella ./charts/umbrella
   kubectl get externalsecrets -n umbrella
   ```

## Next Steps

- Review [Troubleshooting](troubleshooting.md) for service-specific issues
- Check [Configuration Reference](configuration.md) for detailed configuration options
- See [Vault Setup](vault-setup.md) for Vault policy configuration

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

