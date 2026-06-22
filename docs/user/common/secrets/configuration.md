# Configuration Reference

This document provides a comprehensive reference for configuring the External Secrets Operator and HashiCorp Vault
integration in the Tractus-X Umbrella chart.

## Configuration Overview

The secrets management system is configured through several key areas:

- **External Secrets Operator**: Core operator configuration
- **Vault Integration**: HashiCorp Vault connection settings
- **SecretStore**: Vault backend configuration
- **ExternalSecrets**: Individual secret definitions
- **Service Integration**: Service-specific secret references

## External Secrets Operator Configuration

### Basic Configuration

```yaml
# Enable/disable External Secrets Operator
external-secrets:
  enabled: true
```

### Advanced ESO Configuration

```yaml
external-secrets:
  enabled: true

  # ESO deployment configuration
  replicaCount: 2

  # Resource limits
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 10m
      memory: 32Mi

  # Security context
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 65534

  # Service monitor for Prometheus
  serviceMonitor:
    enabled: true
    interval: 30s
    scrapeTimeout: 25s
```

## Vault Configuration

### Basic Vault Configuration

```yaml
vault:
  # Enable Vault integration
  enabled: true

  # Vault server URL
  server: "http://umbrella-infra-vault:8200"

  # KV mount path
  path: "secret"

  # KV version (v1 or v2)
  version: "v2"

  # Vault namespace (Enterprise feature)
  namespace: ""
```

### Production Vault Configuration

```yaml
vault:
  enabled: true
  server: "https://vault.company.com:8200"
  path: "tractus-x"
  version: "v2"
  namespace: "production"

  # TLS configuration
  tls:
    enabled: true
    # CA certificate for Vault server verification
    caCert: |
      -----BEGIN CERTIFICATE-----
      MIIDXTCCAkWgAwIBAgIJAKoK/heBjcOuMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV
      ...
      -----END CERTIFICATE-----
```

## Authentication Configuration

### Token Authentication

```yaml
vault:
  auth:
    method: "token"
    tokenSecret:
      # Name of the Kubernetes secret containing the token
      name: "vault-token"
      # Key within the secret
      key: "token"
      # Optional: namespace of the token secret
      namespace: "vault-system"
```

### AppRole Authentication

```yaml
vault:
  auth:
    method: "appRole"
    appRole:
      # AppRole auth mount path
      path: "approle"
      # Role ID for the AppRole
      roleId: "12345678-1234-1234-1234-123456789012"
      # Secret reference for Secret ID
      secretRef:
        name: "vault-approle-secret"
        key: "secret-id"
        namespace: "vault-system"
```

### Kubernetes Authentication

```yaml
vault:
  auth:
    method: "kubernetes"
    kubernetes:
      # Kubernetes auth mount path
      mountPath: "kubernetes"
      # Vault role for the service account
      role: "external-secrets"
      # Service account token path
      serviceAccountRef:
        name: "external-secrets"
        namespace: "external-secrets-system"
```

## SecretStore Configuration

### Basic SecretStore

```yaml
vault:
  secretStore:
    # Name of the SecretStore resource
    name: "vault-store"

    # Annotations for the SecretStore
    annotations:
      external-secrets.io/disable-maintenance-checks: "true"

    # Labels for the SecretStore
    labels:
      environment: "production"
      team: "platform"
```

### ClusterSecretStore Configuration

For cluster-wide secret access:

```yaml
vault:
  # Use ClusterSecretStore instead of SecretStore
  clusterSecretStore:
    enabled: true
    name: "vault-cluster-store"

    # Allowed namespaces
    conditions:
      - namespaces:
          - "umbrella"
          - "umbrella-dev"
          - "umbrella-staging"
```

## ExternalSecret Configuration

### Basic ExternalSecret

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: umbrella
spec:
  # Refresh interval for secret synchronization
  refreshInterval: 1h

  # Reference to SecretStore
  secretStoreRef:
    name: vault-store
    kind: SecretStore

  # Target Kubernetes secret
  target:
    name: database-credentials
    creationPolicy: Owner
    type: Opaque

  # Secret data mapping
  data:
    - secretKey: username
      remoteRef:
        key: database/credentials
        property: username
    - secretKey: password
      remoteRef:
        key: database/credentials
        property: password
```

### Advanced ExternalSecret with Templates

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: application-config
  namespace: umbrella
spec:
  refreshInterval: 30m
  secretStoreRef:
    name: vault-store
    kind: SecretStore
  target:
    name: application-config
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        # Template with multiple secrets
        config.yaml: |
          database:
            host: {{ .database_host }}
            port: {{ .database_port }}
            username: {{ .database_username }}
            password: {{ .database_password }}
          api:
            key: {{ .api_key }}
            secret: {{ .api_secret }}
  data:
    - secretKey: database_host
      remoteRef:
        key: database/config
        property: host
    - secretKey: database_port
      remoteRef:
        key: database/config
        property: port
    - secretKey: database_username
      remoteRef:
        key: database/credentials
        property: username
    - secretKey: database_password
      remoteRef:
        key: database/credentials
        property: password
    - secretKey: api_key
      remoteRef:
        key: api/credentials
        property: key
    - secretKey: api_secret
      remoteRef:
        key: api/credentials
        property: secret
```

## Service Integration Examples

### CentralIDP Configuration

```yaml
centralidp:
  keycloak:
    auth:
      # Use external secret for admin password
      existingSecret: "umbrella-centralidp"
    postgresql:
      auth:
        # Use external secret for database credentials
        existingSecret: "umbrella-centralidp-postgresql"

  realmSeeding:
    clients:
      # Use external secret for client secrets
      existingSecret: "umbrella-centralidp-clients"
    serviceAccounts:
      # Use external secret for service account credentials
      existingSecret: "umbrella-centralidp-base-service-accounts"
```

### Data Consumer Configuration

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

### Portal Configuration

```yaml
portal:
  backend:
    keycloak:
      secret: "portal-backend-keycloak"
    mailing:
      secret: "portal-backend-mailing"
    interfaces:
      secret: "portal-backend-interfaces"
  postgresql:
    auth:
      existingSecret: "portal-postgres"
```

## Complete Configuration Examples

### Development Environment

```yaml
# values-dev.yaml
external-secrets:
  enabled: true

vault:
  enabled: false  # Use fake secrets for development

# Service configurations using external secrets
centralidp:
  keycloak:
    auth:
      existingSecret: "umbrella-centralidp"
    postgresql:
      auth:
        existingSecret: "umbrella-centralidp-postgresql"

# External secrets definitions (fake mode)
externalSecrets:
  umbrella-centralidp:
    admin-password: "dev-admin-password"

  umbrella-centralidp-postgresql:
    postgres-password: "dev-db-password"
    password: "dev-db-password"
```

### Staging Environment

```yaml
# values-staging.yaml
external-secrets:
  enabled: true

vault:
  enabled: true
  server: "https://vault-staging.company.com:8200"
  path: "staging/tractus-x"
  version: "v2"

  auth:
    method: "appRole"
    appRole:
      path: "approle"
      roleId: "staging-role-id"
      secretRef:
        name: "vault-approle-secret"
        key: "secret-id"

# Service configurations remain the same
centralidp:
  keycloak:
    auth:
      existingSecret: "umbrella-centralidp"
    postgresql:
      auth:
        existingSecret: "umbrella-centralidp-postgresql"
```

### Production Environment

```yaml
# values-production.yaml
external-secrets:
  enabled: true
  replicaCount: 3
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi

vault:
  enabled: true
  server: "https://vault.company.com:8200"
  path: "production/tractus-x"
  version: "v2"
  namespace: "production"

  tls:
    enabled: true
    caCert: |
      -----BEGIN CERTIFICATE-----
      # Production CA certificate
      -----END CERTIFICATE-----

  auth:
    method: "kubernetes"
    kubernetes:
      mountPath: "kubernetes"
      role: "tractus-x-production"
      serviceAccountRef:
        name: "external-secrets"
        namespace: "external-secrets-system"

  secretStore:
    name: "vault-production-store"
    annotations:
      external-secrets.io/disable-maintenance-checks: "false"
    labels:
      environment: "production"
      compliance: "required"

# High-security service configurations
centralidp:
  keycloak:
    auth:
      existingSecret: "umbrella-centralidp"
    postgresql:
      auth:
        existingSecret: "umbrella-centralidp-postgresql"
```

## Secret Refresh Configuration

### Refresh Intervals

```yaml
# Different refresh intervals for different secret types
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: high-frequency-secrets
spec:
  refreshInterval: 5m  # High frequency for critical secrets

---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: standard-secrets
spec:
  refreshInterval: 1h  # Standard frequency

---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: low-frequency-secrets
spec:
  refreshInterval: 24h  # Low frequency for stable secrets
```

### Force Refresh

```yaml
# Force immediate refresh using annotations
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: force-refresh-secret
  annotations:
    force-sync: "2024-08-08T14:13:00Z"
spec:
  refreshInterval: 1h
```

## Error Handling Configuration

### Retry Configuration

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: retry-config-secret
spec:
  refreshInterval: 1h

  # Retry configuration
  retrySettings:
    maxRetries: 5
    retryInterval: 30s
    retryBackoff: exponential
```

### Fallback Secrets

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: fallback-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-store
    kind: SecretStore
  target:
    name: application-secret
    creationPolicy: Owner

  # Primary secret source
  data:
    - secretKey: api-key
      remoteRef:
        key: api/production
        property: key

  # Fallback configuration
  fallback:
    - secretKey: api-key
      value: "fallback-api-key"
```

## Monitoring Configuration

### Metrics and Observability

```yaml
external-secrets:
  enabled: true

  # Enable metrics
  metrics:
    enabled: true
    port: 8080

  # Service monitor for Prometheus
  serviceMonitor:
    enabled: true
    interval: 30s
    path: /metrics
    labels:
      monitoring: "prometheus"
```

### Alerting Configuration

```yaml
# PrometheusRule for External Secrets alerts
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: external-secrets-alerts
spec:
  groups:
    - name: external-secrets
      rules:
        - alert: ExternalSecretSyncFailure
          expr: external_secrets_sync_calls_error > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "External Secret sync failure"
            description: "External Secret {{ $labels.name }} in namespace {{ $labels.namespace }} failed to sync"

        - alert: ExternalSecretNotReady
          expr: external_secrets_status{condition="Ready"} == 0
          for: 10m
          labels:
            severity: critical
          annotations:
            summary: "External Secret not ready"
            description: "External Secret {{ $labels.name }} in namespace {{ $labels.namespace }} is not ready"
```

## Security Configuration

### RBAC Configuration

```yaml
# ServiceAccount for External Secrets Operator
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-secrets
  namespace: external-secrets-system

---
# ClusterRole for External Secrets Operator
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: external-secrets
rules:
  - apiGroups: [ "" ]
    resources: [ "secrets" ]
    verbs: [ "create", "update", "delete", "get", "list", "watch" ]
  - apiGroups: [ "external-secrets.io" ]
    resources: [ "externalsecrets", "secretstores", "clustersecretstores" ]
    verbs: [ "get", "list", "watch" ]

---
# ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: external-secrets
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-secrets
subjects:
  - kind: ServiceAccount
    name: external-secrets
    namespace: external-secrets-system
```

### Network Policies

```yaml
# Network policy for External Secrets Operator
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: external-secrets-network-policy
  namespace: external-secrets-system
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: external-secrets
  policyTypes:
    - Ingress
    - Egress
  egress:
    # Allow access to Vault
    - to:
        - namespaceSelector:
            matchLabels:
              name: vault
      ports:
        - protocol: TCP
          port: 8200
    # Allow access to Kubernetes API
    - to: [ ]
      ports:
        - protocol: TCP
          port: 443
```

## Troubleshooting Configuration

### Debug Configuration

```yaml
external-secrets:
  enabled: true

  # Enable debug logging
  log:
    level: debug
    format: json

  # Enable development mode
  development: true
```

### Validation Configuration

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: validated-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-store
    kind: SecretStore
  target:
    name: validated-secret
    creationPolicy: Owner

  # Validation rules
  data:
    - secretKey: password
      remoteRef:
        key: database/credentials
        property: password
      # Validation: ensure password is not empty
      validation:
        required: true
        minLength: 8
```

## Next Steps

- Review [Connected Services](connected-services.md) for service-specific configurations
- Check [Troubleshooting](troubleshooting.md) for common configuration issues
- See [Vault Setup](vault-setup.md) for Vault-specific configuration details

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

