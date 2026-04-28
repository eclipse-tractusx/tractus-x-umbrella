# Data Exchange with Dual IdentityHub Architecture

## Overview

This document describes a **demonstration setup** for data exchange using two separate IdentityHub instances - one for the data consumer and one for the data provider. This configuration is designed to **showcase how IdentityHub works in a data exchange scenario**, demonstrating a decentralized identity and trust model where each participant manages their own identity infrastructure.

**Purpose:** This setup serves as a reference implementation and testing environment to validate that IdentityHub can successfully handle identity and trust operations (DID resolution, credential management, STS token issuance) within the context of EDC-based data exchange between multiple participants.

## Chart Structure and Dependencies

### Umbrella Chart Hierarchy

The data exchange setup leverages Helm chart dependencies to create a modular, composable architecture:

```
umbrella (v3.15.3)
├── dataconsumerOne (alias of tx-data-provider v0.4.6)
│   ├── digital-twin-bundle (v1.1.0)
│   ├── data-persistence-layer-bundle (v1.0.0)
│   ├── dataspace-connector-bundle (v1.2.2)
│   │   └── tractusx-connector (EDC)
│   └── identity-and-trust-bundle (v1.1.3)
│       ├── ssi-dim-wallet-stub (disabled)
│       └── tractusx-identityhub (v0.2.1)
│
├── tx-data-provider (v0.4.6)
│   ├── digital-twin-bundle (v1.1.0)
│   ├── data-persistence-layer-bundle (v1.0.0)
│   ├── dataspace-connector-bundle (v1.2.2)
│   │   └── tractusx-connector (EDC)
│   └── identity-and-trust-bundle (v1.1.3)
│       ├── ssi-dim-wallet-stub (disabled)
│       └── tractusx-identityhub (v0.2.1)
│
└── bdrs-server-memory (v0.7.0-SNAPSHOT)
```

**Note:** The `ssi-dim-wallet-stub` is available as a dependency in `identity-and-trust-bundle` but is disabled in this configuration. Only the `tractusx-identityhub` component is used for identity and trust operations.

### Key Design Principles

**Embedded Identity Infrastructure**: The `tx-data-provider` chart includes `identity-and-trust-bundle` as a dependency, enabling each participant to have their own dedicated IdentityHub instance.

> [!NOTE]
> This represents an initial working version of IdentityHub-based data exchange. While the configuration and architecture may not be the best structure whise, it will remain this way just to have a template of a working data exchange with identityhub.

### Environment Variables

Critical environment variables for IATP integration:

- `TX_IAM_IATP_CREDENTIALSERVICE_URL`: Points to the participant's IdentityHub credential service
- `EDC_IAM_DID_WEB_USE_HTTPS`: Set to `false` for local development
- `EDC_IAM_CREDENTIAL_REVOCATION_MIMETYPE`: Set to `application/json`

## Deployment

### Update Chart Dependencies

Before installing, ensure all chart dependencies are downloaded:

```bash
cd charts/umbrella
helm install umbrella -f ./values-adopter-data-exchange-identityhub.yaml
```

## Known Issues / Modifications

### Custom Attestation Claims Data Table

A new `custom_attestation_claims` data table has been created to support custom claims in attestation processes. This table enables database-backed attestation for credential issuance, allowing custom claims to be dynamically included in issued verifiable credentials.

#### Table Schema

| Column | Type | Description |
|--------|------|-------------|
| `holder_id` | VARCHAR (PK) | Holder/participant identifier (must match DID) |
| `holder_identifier` | VARCHAR | Holder DID |
| `member_of` | VARCHAR | Membership identifier (e.g., "Catena-X") |
| `bpn` | VARCHAR(50) | Business Partner Number |
| `group_name` | VARCHAR(100) | Group/framework name |
| `use_case` | TEXT | Use case identifier |
| `contract_template` | VARCHAR(255) | Contract template URL |
| `contract_version` | VARCHAR(50) | Contract version |
| `created_date` | BIGINT | POSIX timestamp (creation) |
| `last_modified_date` | BIGINT | POSIX timestamp (last update) |

#### Purpose

This table stores custom claims that can be referenced during credential issuance through database attestations. When creating credential definitions, you can configure mappings that pull data from this table and include it in the issued credentials.

#### Sample Data

The migration includes pre-populated test data for both the consumer and provider participants:

```sql
-- Consumer participant sample data
INSERT INTO custom_attestation_claims (
    holder_id, holder_identifier, member_of, bpn, 
    group_name, use_case, contract_template, contract_version,
    created_date, last_modified_date
) VALUES (
    'did:web:identityhub.consumer.tx.test:BPNL00000003AZQP',
    'did:web:identityhub.consumer.tx.test:BPNL00000003AZQP',
    'Catena-X',
    'BPNL00000003AZQP',
    'UseCaseFramework',
    'DataExchangeGovernance',
    'https://example.org/temp-1',
    '1.0',
    EXTRACT(EPOCH FROM NOW()) * 1000,
    EXTRACT(EPOCH FROM NOW()) * 1000
);

-- Provider participant sample data
INSERT INTO custom_attestation_claims (
    holder_id, holder_identifier, member_of, bpn,
    group_name, use_case, contract_template, contract_version,
    created_date, last_modified_date
) VALUES (
    'did:web:identityhub.provider.tx.test:BPNS00000000AAAA',
    'did:web:identityhub.provider.tx.test:BPNS00000000AAAA',
    'Catena-X',
    'BPNS00000000AAAA',
    'UseCaseFramework',
    'DataExchangeGovernance',
    'https://example.org/temp-1',
    '1.0',
    EXTRACT(EPOCH FROM NOW()) * 1000,
    EXTRACT(EPOCH FROM NOW()) * 1000
);
```

#### Configuration

The datasource is configured in the IssuerService Helm chart:

```yaml
edc.sql.store.customattestations.datasource: "customattestations"
edc.datasource.customattestations.url: jdbc:postgresql://...
edc.datasource.customattestations.user: <username>
edc.datasource.customattestations.password: <password>
org.eclipse.tractusx.edc.postgresql.migration.customattestations.enabled: "true"
```

### BDRS Server Version Issue

This setup uses a **local build** of `bdrs-server-memory` from the main branch (`v0.7.0-SNAPSHOT`) instead of the published version `v0.5.7`.

**Reason**: The published version `v0.5.7` lacks certain configuration settings and features that are required for this IdentityHub-based data exchange setup. The necessary updates are only available in the main branch.

**Configuration**:
```yaml
env:
  EDC_IAM_CREDENTIAL_REVOCATION_MIMETYPE: application/json
```

### IdentityHub ConfigMap Naming Issue

This setup uses a **local build** of `tractusx-identityhub` charts instead of the published version due to ConfigMap naming conflicts.

**Problem**: The published IdentityHub Helm charts used **static ConfigMap names** instead of dynamic names based on the release name. This prevented deploying multiple IdentityHub instances in the same namespace, as the ConfigMaps would conflict.

**Solution**: The ConfigMap templates were updated to use dynamic naming with the release name prefix (e.g., `{{ include "identityhub.fullname" . }}-config`), allowing multiple independent IdentityHub instances to coexist.

**Impact**: 
- Consumer IdentityHub instance can be deployed alongside Provider IdentityHub instance
- Each instance maintains its own isolated configuration
- No ConfigMap name collisions in the same Kubernetes namespace

**Configuration**:
```yaml
identity-and-trust-bundle:
  tractusx-identityhub:
    nameOverride: identityhubconsumer-1  # Unique name per instance
```

**Note**: Future releases of the IdentityHub Helm charts should include this fix, allowing use of the official chart repository.
