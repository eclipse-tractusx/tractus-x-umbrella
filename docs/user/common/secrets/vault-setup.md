# HashiCorp Vault Setup

This guide covers the setup and configuration of HashiCorp Vault for use with the Tractus-X Umbrella External Secrets
integration.

## Overview

HashiCorp Vault serves as the external secret store for the Tractus-X Umbrella deployment. This guide covers:

- Vault installation and configuration
- Authentication setup
- Policy configuration
- Secret management
- Integration with External Secrets Operator

## Vault Installation

### Option 1: Using Umbrella Infrastructure Chart

The easiest way to deploy Vault is using the umbrella-infrastructure chart:

```bash
# Add the Helm repository
helm repo add tractus-x-umbrella https://eclipse-tractusx.github.io/tractus-x-umbrella
helm repo update

# Deploy Vault
helm install umbrella-infra tractus-x-umbrella/umbrella-infrastructure \
  --namespace umbrella-infra \
  --create-namespace \
  --set vault.enabled=true \
  --set vault.server.dev.enabled=true  # For development only
```

### Option 2: Using Official HashiCorp Vault Chart

For production deployments, use the official HashiCorp Vault chart:

```bash
# Add HashiCorp Helm repository
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Create values file for production
cat > vault-values.yaml << EOF
server:
  ha:
    enabled: true
    replicas: 3
  dataStorage:
    enabled: true
    size: 10Gi
  auditStorage:
    enabled: true
    size: 10Gi
ui:
  enabled: true
  serviceType: "ClusterIP"
EOF

# Deploy Vault
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --values vault-values.yaml
```

### Option 3: External Vault Instance

If using an external Vault instance, ensure:

- Vault is accessible from your Kubernetes cluster
- Network policies allow communication
- Proper authentication is configured

## Vault Initialization

### Development Mode (Auto-initialized)

When using `dev.enabled=true`, Vault is automatically initialized with:

- Root token: `root`
- Unsealed automatically
- KV v2 secrets engine enabled at `secret/`

### Production Mode Initialization

For production Vault deployments:

```bash
# Initialize Vault (run once)
kubectl exec vault-0 -n vault -- vault operator init \
  -key-shares=5 \
  -key-threshold=3 \
  -format=json > vault-init.json

# Extract unseal keys and root token
UNSEAL_KEY_1=$(cat vault-init.json | jq -r '.unseal_keys_b64[0]')
UNSEAL_KEY_2=$(cat vault-init.json | jq -r '.unseal_keys_b64[1]')
UNSEAL_KEY_3=$(cat vault-init.json | jq -r '.unseal_keys_b64[2]')
ROOT_TOKEN=$(cat vault-init.json | jq -r '.root_token')

# Unseal Vault (repeat for each replica)
kubectl exec vault-0 -n vault -- vault operator unseal $UNSEAL_KEY_1
kubectl exec vault-0 -n vault -- vault operator unseal $UNSEAL_KEY_2
kubectl exec vault-0 -n vault -- vault operator unseal $UNSEAL_KEY_3
```

## Authentication Configuration

### Token Authentication (Development)

Token authentication is suitable for development environments:

```bash
# Set environment variables
export VAULT_ADDR="http://vault.vault.svc.cluster.local:8200"
export VAULT_TOKEN="root"  # Use your actual root token

# Create a token for External Secrets Operator
vault token create -policy=external-secrets -ttl=24h
```

### AppRole Authentication (Production)

AppRole authentication is recommended for production:

```bash
# Enable AppRole auth method
vault auth enable approle

# Create policy for External Secrets Operator
vault policy write external-secrets - << EOF
# Allow reading secrets from the secret/ path
path "secret/data/*" {
  capabilities = ["read"]
}

# Allow listing secrets
path "secret/metadata/*" {
  capabilities = ["list"]
}
EOF

# Create AppRole
vault write auth/approle/role/external-secrets \
  token_policies="external-secrets" \
  token_ttl=1h \
  token_max_ttl=4h

# Get Role ID
vault read auth/approle/role/external-secrets/role-id

# Generate Secret ID
vault write -f auth/approle/role/external-secrets/secret-id
```

## Vault Policies

### External Secrets Operator Policy

Create a dedicated policy for the External Secrets Operator:

```hcl
# external-secrets-policy.hcl
# Read access to all secrets under secret/
path "secret/data/*" {
  capabilities = ["read"]
}

# List access to secret metadata
path "secret/metadata/*" {
  capabilities = ["list"]
}

# Allow token self-renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Allow token lookup
path "auth/token/lookup-self" {
  capabilities = ["read"]
}
```

Apply the policy:

```bash
vault policy write external-secrets external-secrets-policy.hcl
```

### Service-Specific Policies

For enhanced security, create service-specific policies:

```bash
# Policy for CentralIDP secrets only
vault policy write centralidp - << EOF
path "secret/data/umbrella-centralidp*" {
  capabilities = ["read"]
}
path "secret/metadata/umbrella-centralidp*" {
  capabilities = ["list"]
}
EOF

# Policy for database secrets only
vault policy write databases - << EOF
path "secret/data/*-db" {
  capabilities = ["read"]
}
path "secret/data/*-postgresql" {
  capabilities = ["read"]
}
EOF
```

## Secret Management

### Using the Vault-Secrets-Setup Script

The recommended way to populate Vault with Tractus-X secrets:

```bash
# Navigate to dataseeding directory
cd dataseeding

# Install dependencies
pip install PyYAML requests

# Set Vault connection
export VAULT_ADDR="http://vault.vault.svc.cluster.local:8200"
export VAULT_TOKEN="your-token"

# Dry run to verify
python vault-secrets-setup.py --dry-run

# Populate secrets
python vault-secrets-setup.py
```

### Manual Secret Creation

For individual secrets:

```bash
# Create a database secret
vault kv put secret/umbrella-centralidp-postgresql \
  postgres-password="dbpasswordcentralidp" \
  password="dbpasswordcentralidp"

# Create service account secrets
vault kv put secret/umbrella-centralidp-base-service-accounts \
  sa-cl1-reg-2="changeme1" \
  sa-cl2-01="changeme" \
  sa-cl2-02="changeme"
```

### Secret Versioning

Vault KV v2 supports secret versioning:

```bash
# View secret versions
vault kv metadata get secret/umbrella-centralidp-postgresql

# Get specific version
vault kv get -version=2 secret/umbrella-centralidp-postgresql

# Delete specific version
vault kv delete -versions=1 secret/umbrella-centralidp-postgresql

# Undelete version
vault kv undelete -versions=1 secret/umbrella-centralidp-postgresql
```

## Vault Configuration for External Secrets

### SecretStore Configuration

The SecretStore resource connects External Secrets Operator to Vault:

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: vault-store
  namespace: umbrella
spec:
  provider:
    vault:
      server: "http://vault.vault.svc.cluster.local:8200"
      path: "secret"
      version: "v2"
      auth:
        # Token authentication
        tokenSecretRef:
          name: "vault-token"
          key: "token"

        # OR AppRole authentication
        # appRole:
        #   path: "approle"
        #   roleId: "your-role-id"
        #   secretRef:
        #     name: "vault-approle-secret"
        #     key: "secret-id"
```

### ExternalSecret Configuration

Example ExternalSecret resource:

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: umbrella-centralidp-postgresql
  namespace: umbrella
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-store
    kind: SecretStore
  target:
    name: umbrella-centralidp-postgresql
    creationPolicy: Owner
  data:
    - secretKey: postgres-password
      remoteRef:
        key: umbrella-centralidp-postgresql
        property: postgres-password
    - secretKey: password
      remoteRef:
        key: umbrella-centralidp-postgresql
        property: password
```

## High Availability Setup

### Vault HA Configuration

For production deployments, configure Vault in HA mode:

```yaml
# vault-ha-values.yaml
server:
  ha:
    enabled: true
    replicas: 3
    raft:
      enabled: true
      setNodeId: true
      config: |
        ui = true
        listener "tcp" {
          tls_disable = 1
          address = "[::]:8200"
          cluster_address = "[::]:8201"
        }
        storage "raft" {
          path = "/vault/data"
        }
        service_registration "kubernetes" {}
```

### Load Balancer Configuration

Configure a load balancer for Vault access:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vault-lb
  namespace: vault
spec:
  type: LoadBalancer
  ports:
    - port: 8200
      targetPort: 8200
      protocol: TCP
  selector:
    app.kubernetes.io/name: vault
    component: server
```

## Security Hardening

### TLS Configuration

Enable TLS for production:

```yaml
# vault-tls-values.yaml
server:
  extraEnvironmentVars:
    VAULT_CACERT: /vault/userconfig/vault-tls/ca.crt
  volumes:
    - name: vault-tls
      secret:
        secretName: vault-tls
  volumeMounts:
    - name: vault-tls
      mountPath: /vault/userconfig/vault-tls
  ha:
    config: |
      listener "tcp" {
        address = "[::]:8200"
        cluster_address = "[::]:8201"
        tls_cert_file = "/vault/userconfig/vault-tls/tls.crt"
        tls_key_file = "/vault/userconfig/vault-tls/tls.key"
        tls_client_ca_file = "/vault/userconfig/vault-tls/ca.crt"
      }
```

### Network Policies

Restrict network access to Vault:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: vault-network-policy
  namespace: vault
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: vault
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: umbrella
        - namespaceSelector:
            matchLabels:
              name: external-secrets-system
      ports:
        - protocol: TCP
          port: 8200
```

## Monitoring and Observability

### Vault Metrics

Enable Prometheus metrics:

```hcl
# vault-config.hcl
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}
```

### Audit Logging

Enable audit logging:

```bash
# Enable file audit device
vault audit enable file file_path=/vault/logs/audit.log

# Enable syslog audit device
vault audit enable syslog tag="vault" facility="AUTH"
```

### Health Checks

Configure health check endpoints:

```bash
# Check Vault status
curl http://vault:8200/v1/sys/health

# Check seal status
curl http://vault:8200/v1/sys/seal-status
```

## Backup and Recovery

### Vault Snapshots

Create regular snapshots:

```bash
# Create snapshot
vault operator raft snapshot save backup.snap

# Restore from snapshot
vault operator raft snapshot restore backup.snap
```

### Automated Backup Script

```bash
#!/bin/bash
# vault-backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/vault"
BACKUP_FILE="$BACKUP_DIR/vault_snapshot_$DATE.snap"

mkdir -p $BACKUP_DIR
vault operator raft snapshot save $BACKUP_FILE

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "vault_snapshot_*.snap" -mtime +7 -delete
```

## Troubleshooting

### Common Issues

1. **Vault Sealed**:
   ```bash
   kubectl exec vault-0 -n vault -- vault status
   kubectl exec vault-0 -n vault -- vault operator unseal <key>
   ```

2. **Authentication Failures**:
   ```bash
   vault auth list
   vault token lookup
   ```

3. **Policy Issues**:
   ```bash
   vault policy list
   vault policy read external-secrets
   ```

### Debug Commands

```bash
# Check Vault logs
kubectl logs vault-0 -n vault

# Check External Secrets Operator logs
kubectl logs -n external-secrets-system deployment/external-secrets

# Test Vault connectivity
kubectl run vault-test --rm -it --image=vault:latest -- sh
```

## Next Steps

- Review [Configuration Reference](configuration.md) for complete configuration options
- Check [Connected Services](connected-services.md) for service-specific configurations
- See [Troubleshooting](troubleshooting.md) for additional troubleshooting guidance

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

