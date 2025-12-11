# Deployment Guide

This guide provides step-by-step instructions for deploying the Tractus-X Umbrella with External Secrets Operator and
HashiCorp Vault integration.

## Prerequisites

Before deploying the secrets management system, ensure you have:

- Kubernetes cluster (v1.20+)
- Helm 3.x installed
- kubectl configured for your cluster
- Access to a HashiCorp Vault instance (or ability to deploy one)
- Python 3.6+ (for the vault-secrets-setup script)

## Deployment Options

The Tractus-X Umbrella supports three deployment modes for secrets management:

1. **Production Mode**: Full External Secrets Operator with HashiCorp Vault
2. **Development Mode**: External Secrets Operator with fake secrets for testing
3. **Legacy Mode**: Traditional Kubernetes secrets (no external secrets)

## Option 1: Production Deployment with Vault

### Step 1: Deploy HashiCorp Vault (Optional)

If you don't have an existing Vault instance, you can deploy one using the umbrella-infrastructure chart:

```bash
# Add the umbrella-infrastructure chart
helm repo add tractus-x-umbrella https://eclipse-tractusx.github.io/tractus-x-umbrella

# Deploy Vault with the infrastructure chart
helm install umbrella-infra tractus-x-umbrella/umbrella-infrastructure \
  --namespace umbrella-infra \
  --create-namespace \
  --set vault.enabled=true
```

### Step 2: Configure Vault Access

Set up environment variables for Vault access:

```bash
# Set Vault server address
export VAULT_ADDR="http://your-vault-server:8200"

# Set Vault token (obtain from your Vault administrator)
export VAULT_TOKEN="your-vault-token"
```

### Step 3: Populate Vault with Secrets

Use the provided script to populate Vault with the required secrets:

```bash
# Navigate to the dataseeding directory
cd dataseeding

# Install Python dependencies
pip install PyYAML requests

# Run dry-run to verify configuration
python vault-secrets-setup.py --dry-run

# Populate Vault with secrets
python vault-secrets-setup.py
```

### Step 4: Create Values File

Create a values file for your deployment:

```yaml
# values-production.yaml
external-secrets:
  enabled: true

vault:
  enabled: true
  server: "http://umbrella-infra-vault:8200"
  path: "secret"
  version: "v2"

  auth:
    method: "token"
    tokenSecret:
      name: "vault-token"
      key: "token"

# Include your specific service configurations
# You can extend values-external-secrets.yaml
```

### Step 5: Deploy the Umbrella Chart

```bash
# Deploy with external secrets enabled
helm install tractus-x-umbrella tractus-x-umbrella/umbrella \
  --namespace umbrella \
  --create-namespace \
  --values values-production.yaml \
  --values charts/umbrella/values-external-secrets.yaml
```

## Option 2: Development Deployment with Fake Secrets

For development and testing environments, you can use fake secrets:

### Step 1: Create Development Values File

```yaml
# values-development.yaml
external-secrets:
  enabled: true

vault:
  enabled: false  # This enables fake secrets mode

# The externalSecrets section from values-external-secrets.yaml
# will be used to create fake ExternalSecret resources
```

### Step 2: Deploy with Fake Secrets

```bash
helm install tractus-x-umbrella tractus-x-umbrella/umbrella \
  --namespace umbrella \
  --create-namespace \
  --values values-development.yaml \
  --values charts/umbrella/values-external-secrets.yaml
```

## Option 3: Legacy Deployment

For backward compatibility, you can disable external secrets entirely:

```yaml
# values-legacy.yaml
external-secrets:
  enabled: false

vault:
  enabled: false
```

```bash
helm install tractus-x-umbrella tractus-x-umbrella/umbrella \
  --namespace umbrella \
  --create-namespace \
  --values values-legacy.yaml
```

## Verification

### Check External Secrets Operator

Verify that the External Secrets Operator is running:

```bash
kubectl get pods -n external-secrets-system
```

### Check SecretStore

Verify that the Vault SecretStore is created and ready:

```bash
kubectl get secretstore -n umbrella
kubectl describe secretstore vault-store -n umbrella
```

### Check ExternalSecrets

Verify that ExternalSecret resources are created and syncing:

```bash
kubectl get externalsecrets -n umbrella
kubectl describe externalsecret umbrella-centralidp-postgresql -n umbrella
```

### Check Generated Secrets

Verify that Kubernetes secrets are being created:

```bash
kubectl get secrets -n umbrella | grep umbrella-
```

## Upgrading

### Upgrading from Legacy to External Secrets

1. **Backup existing secrets**:
   ```bash
   kubectl get secrets -n umbrella -o yaml > backup-secrets.yaml
   ```

2. **Deploy Vault and populate with secrets**:
   Follow steps 1-3 from the production deployment

3. **Upgrade with external secrets enabled**:
   ```bash
   helm upgrade tractus-x-umbrella tractus-x-umbrella/umbrella \
     --namespace umbrella \
     --values values-production.yaml \
     --values charts/umbrella/values-external-secrets.yaml
   ```

### Upgrading External Secrets Configuration

To update secret values in Vault:

1. **Update secrets in Vault** using the vault-secrets-setup script
2. **Force refresh** of ExternalSecrets:
   ```bash
   kubectl annotate externalsecret umbrella-centralidp-postgresql \
     force-sync=$(date +%s) -n umbrella
   ```

## Authentication Methods

### Token Authentication (Default)

Token authentication is the simplest method for getting started:

```yaml
vault:
  auth:
    method: "token"
    tokenSecret:
      name: "vault-token"
      key: "token"
```

The token secret is automatically created by the chart with a default token for development.

### AppRole Authentication (Recommended for Production)

AppRole provides more secure authentication for production environments:

```yaml
vault:
  auth:
    method: "appRole"
    appRole:
      path: "approle"
      roleId: "your-role-id"
      secretRef:
        name: "vault-approle-secret"
        key: "secret-id"
```

## Monitoring and Observability

### External Secrets Operator Metrics

The External Secrets Operator exposes Prometheus metrics:

```bash
kubectl port-forward -n external-secrets-system \
  svc/external-secrets-webhook 8080:8080
```

Access metrics at: `http://localhost:8080/metrics`

### Vault Audit Logs

Enable Vault audit logging for compliance and troubleshooting:

```bash
vault audit enable file file_path=/vault/logs/audit.log
```

## Best Practices

1. **Use HTTPS in Production**: Always configure Vault with TLS certificates
2. **Implement Vault Policies**: Create specific policies for the External Secrets Operator
3. **Regular Token Rotation**: Implement automated token rotation
4. **Monitor Secret Sync**: Set up alerts for failed secret synchronization
5. **Backup Vault Data**: Implement regular Vault backups
6. **Use Namespaces**: Deploy different environments in separate namespaces

## Next Steps

- Configure [Vault Setup](vault-setup.md) for advanced Vault configuration
- Review [Configuration Reference](configuration.md) for all available options
- Check [Connected Services](connected-services.md) for service-specific configurations
- See [Troubleshooting](troubleshooting.md) for common issues and solutions