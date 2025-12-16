# Troubleshooting

This guide provides solutions to common issues encountered when using the External Secrets Operator and HashiCorp Vault
integration in the Tractus-X Umbrella.

## Common Issues and Solutions

### External Secrets Operator Issues

#### 1. External Secrets Operator Not Starting

**Symptoms:**

- ESO pods in `CrashLoopBackOff` or `Pending` state
- Error messages about missing CRDs or permissions

**Diagnosis:**

```bash
# Check ESO pod status
kubectl get pods -n external-secrets-system

# Check ESO logs
kubectl logs -n external-secrets-system deployment/external-secrets

# Check CRDs
kubectl get crd | grep external-secrets
```

**Solutions:**

1. **Missing CRDs:**
   ```bash
   # Install External Secrets Operator CRDs
   kubectl apply -f https://raw.githubusercontent.com/external-secrets/external-secrets/main/deploy/crds/bundle.yaml
   ```

2. **RBAC Issues:**
   ```bash
   # Check service account and RBAC
   kubectl get serviceaccount -n external-secrets-system
   kubectl get clusterrole external-secrets
   kubectl get clusterrolebinding external-secrets
   ```

3. **Resource Constraints:**
   ```yaml
   # Increase resource limits
   external-secrets:
     resources:
       limits:
         cpu: 200m
         memory: 256Mi
       requests:
         cpu: 50m
         memory: 64Mi
   ```

#### 2. SecretStore Connection Issues

**Symptoms:**

- SecretStore shows `Invalid` or `NotReady` status
- Error messages about Vault connection failures

**Diagnosis:**

```bash
# Check SecretStore status
kubectl get secretstore -n umbrella
kubectl describe secretstore vault-store -n umbrella

# Check connectivity to Vault
kubectl run vault-test --rm -it --image=curlimages/curl -- sh
# Inside the pod:
curl -k http://umbrella-infra-vault:8200/v1/sys/health
```

**Solutions:**

1. **Incorrect Vault URL:**
   ```yaml
   vault:
     server: "http://umbrella-infra-vault:8200"  # Correct internal URL
   ```

2. **Authentication Issues:**
   ```bash
   # Check if vault token secret exists
   kubectl get secret vault-token -n umbrella
   
   # Verify token is valid
   kubectl exec -it vault-0 -n vault -- vault token lookup
   ```

3. **Network Policies:**
   ```yaml
   # Allow ESO to access Vault
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-eso-to-vault
   spec:
     podSelector:
       matchLabels:
         app.kubernetes.io/name: external-secrets
     egress:
     - to:
       - namespaceSelector:
           matchLabels:
             name: vault
       ports:
       - protocol: TCP
         port: 8200
   ```

### ExternalSecret Issues

#### 3. ExternalSecret Not Syncing

**Symptoms:**

- ExternalSecret shows `SecretSyncError` status
- Kubernetes secret not created or outdated

**Diagnosis:**

```bash
# Check ExternalSecret status
kubectl get externalsecret -n umbrella
kubectl describe externalsecret umbrella-centralidp -n umbrella

# Check events
kubectl get events -n umbrella --field-selector involvedObject.name=umbrella-centralidp
```

**Solutions:**

1. **Secret Not Found in Vault:**
   ```bash
   # Verify secret exists in Vault
   vault kv get secret/umbrella-centralidp
   
   # Create missing secret
   vault kv put secret/umbrella-centralidp admin-password="password"
   ```

2. **Incorrect Secret Path:**
   ```yaml
   # Ensure correct path in ExternalSecret
   data:
     - secretKey: admin-password
       remoteRef:
         key: umbrella-centralidp  # Correct path
         property: admin-password
   ```

3. **Permission Issues:**
   ```bash
   # Check Vault policy
   vault policy read external-secrets
   
   # Test token permissions
   vault kv get secret/umbrella-centralidp
   ```

#### 4. Secret Refresh Issues

**Symptoms:**

- Secrets not updating when changed in Vault
- Old secret values still in use

**Solutions:**

1. **Force Refresh:**
   ```bash
   # Annotate ExternalSecret to force refresh
   kubectl annotate externalsecret umbrella-centralidp \
     force-sync=$(date +%s) -n umbrella
   ```

2. **Adjust Refresh Interval:**
   ```yaml
   spec:
     refreshInterval: 5m  # Reduce interval for more frequent updates
   ```

3. **Check ESO Controller:**
   ```bash
   # Restart ESO controller
   kubectl rollout restart deployment/external-secrets -n external-secrets-system
   ```

### Vault Issues

#### 5. Vault Sealed

**Symptoms:**

- Vault returns 503 Service Unavailable
- Error messages about sealed Vault

**Diagnosis:**

```bash
# Check Vault status
kubectl exec vault-0 -n vault -- vault status
```

**Solutions:**

1. **Unseal Vault:**
   ```bash
   # Unseal with keys (repeat for threshold number of keys)
   kubectl exec vault-0 -n vault -- vault operator unseal <unseal-key-1>
   kubectl exec vault-0 -n vault -- vault operator unseal <unseal-key-2>
   kubectl exec vault-0 -n vault -- vault operator unseal <unseal-key-3>
   ```

2. **Auto-unseal Configuration:**
   ```yaml
   # Configure auto-unseal for production
   server:
     ha:
       config: |
         seal "awskms" {
           region     = "us-west-2"
           kms_key_id = "alias/vault-unseal-key"
         }
   ```

#### 6. Vault Authentication Failures

**Symptoms:**

- 403 Forbidden errors from Vault
- Authentication method failures

**Diagnosis:**

```bash
# Check authentication methods
kubectl exec vault-0 -n vault -- vault auth list

# Test token
kubectl exec vault-0 -n vault -- vault token lookup
```

**Solutions:**

1. **Token Expired:**
   ```bash
   # Create new token
   kubectl exec vault-0 -n vault -- vault token create -policy=external-secrets
   
   # Update token secret
   kubectl create secret generic vault-token \
     --from-literal=token=<new-token> \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

2. **AppRole Issues:**
   ```bash
   # Check AppRole configuration
   kubectl exec vault-0 -n vault -- vault read auth/approle/role/external-secrets
   
   # Generate new secret ID
   kubectl exec vault-0 -n vault -- vault write -f auth/approle/role/external-secrets/secret-id
   ```

### Service Integration Issues

#### 7. Service Cannot Access Secrets

**Symptoms:**

- Services failing to start with authentication errors
- Environment variables not populated

**Diagnosis:**

```bash
# Check if secret exists
kubectl get secret umbrella-centralidp -n umbrella

# Verify secret content
kubectl get secret umbrella-centralidp -o yaml

# Check service configuration
kubectl describe deployment centralidp-keycloak -n umbrella
```

**Solutions:**

1. **Secret Not Created:**
   ```bash
   # Check ExternalSecret status
   kubectl describe externalsecret umbrella-centralidp -n umbrella
   
   # Force sync if needed
   kubectl annotate externalsecret umbrella-centralidp force-sync=$(date +%s)
   ```

2. **Wrong Secret Reference:**
   ```yaml
   # Ensure correct secret name in service config
   keycloak:
     auth:
       existingSecret: "umbrella-centralidp"  # Must match ExternalSecret target name
   ```

3. **Missing Secret Keys:**
   ```bash
   # Check required keys exist
   kubectl get secret umbrella-centralidp -o jsonpath='{.data}' | jq
   ```

#### 8. Database Connection Issues

**Symptoms:**

- Database connection failures
- Services unable to connect to PostgreSQL

**Solutions:**

1. **Check Database Secret:**
   ```bash
   # Verify database secret exists and has correct keys
   kubectl get secret umbrella-centralidp-postgresql -o yaml
   ```

2. **Test Database Connection:**
   ```bash
   # Create test pod to verify connectivity
   kubectl run postgres-test --rm -it --image=postgres:13 -- bash
   # Inside pod:
   PGPASSWORD=<password> psql -h <host> -U <user> -d <database>
   ```

### Performance Issues

#### 9. Slow Secret Synchronization

**Symptoms:**

- Long delays in secret updates
- High resource usage by ESO

**Solutions:**

1. **Optimize Refresh Intervals:**
   ```yaml
   # Use appropriate refresh intervals
   spec:
     refreshInterval: 1h  # Don't refresh too frequently
   ```

2. **Increase ESO Resources:**
   ```yaml
   external-secrets:
     resources:
       limits:
         cpu: 500m
         memory: 512Mi
   ```

3. **Use ClusterSecretStore:**
   ```yaml
   # Reduce overhead with ClusterSecretStore
   vault:
     clusterSecretStore:
       enabled: true
   ```

#### 10. High Memory Usage

**Solutions:**

1. **Limit Secret Size:**
   ```bash
   # Avoid storing large files in secrets
   # Use ConfigMaps for non-sensitive large data
   ```

2. **Optimize Secret Structure:**
   ```yaml
   # Split large secrets into smaller ones
   # Use separate secrets per service
   ```

## Diagnostic Commands

### General Diagnostics

```bash
# Check all External Secrets resources
kubectl get externalsecrets,secretstores,clustersecretstores -A

# Check ESO controller logs
kubectl logs -n external-secrets-system deployment/external-secrets --tail=100

# Check Vault status
kubectl exec vault-0 -n vault -- vault status

# List all secrets in namespace
kubectl get secrets -n umbrella

# Check events for troubleshooting
kubectl get events -n umbrella --sort-by='.lastTimestamp'
```

### Vault Diagnostics

```bash
# Check Vault health
curl -k http://vault:8200/v1/sys/health

# List authentication methods
kubectl exec vault-0 -n vault -- vault auth list

# Check policies
kubectl exec vault-0 -n vault -- vault policy list

# Test secret access
kubectl exec vault-0 -n vault -- vault kv get secret/umbrella-centralidp
```

### Network Diagnostics

```bash
# Test connectivity from ESO to Vault
kubectl exec -n external-secrets-system deployment/external-secrets -- \
  curl -k http://umbrella-infra-vault:8200/v1/sys/health

# Check DNS resolution
kubectl exec -n external-secrets-system deployment/external-secrets -- \
  nslookup umbrella-infra-vault

# Test from application namespace
kubectl run test-pod --rm -it --image=curlimages/curl -n umbrella -- \
  curl -k http://umbrella-infra-vault:8200/v1/sys/health
```

## Debug Mode

### Enable Debug Logging

```yaml
# Enable debug logging for ESO
external-secrets:
  log:
    level: debug
    format: json
```

### Verbose ExternalSecret

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: debug-secret
  annotations:
    external-secrets.io/debug: "true"
spec:
# ... rest of configuration
```

## Monitoring and Alerting

### Prometheus Metrics

```bash
# Check ESO metrics
kubectl port-forward -n external-secrets-system svc/external-secrets-webhook 8080:8080
curl http://localhost:8080/metrics | grep external_secrets
```

### Key Metrics to Monitor

- `external_secrets_sync_calls_total`: Total sync attempts
- `external_secrets_sync_calls_error`: Failed sync attempts
- `external_secrets_status`: Current status of ExternalSecrets

### Sample Alerts

```yaml
# Alert on sync failures
- alert: ExternalSecretSyncFailure
  expr: increase(external_secrets_sync_calls_error[5m]) > 0
  labels:
    severity: warning

# Alert on secrets not ready
- alert: ExternalSecretNotReady
  expr: external_secrets_status{condition="Ready"} == 0
  for: 10m
  labels:
    severity: critical
```

## Recovery Procedures

### Complete Recovery Steps

1. **Backup Current State:**
   ```bash
   kubectl get externalsecrets -o yaml > externalsecrets-backup.yaml
   kubectl get secrets -o yaml > secrets-backup.yaml
   ```

2. **Reset External Secrets:**
   ```bash
   # Delete and recreate ExternalSecrets
   kubectl delete externalsecrets --all -n umbrella
   kubectl apply -f externalsecrets-backup.yaml
   ```

3. **Restart Components:**
   ```bash
   # Restart ESO
   kubectl rollout restart deployment/external-secrets -n external-secrets-system
   
   # Restart affected services
   kubectl rollout restart deployment/centralidp-keycloak -n umbrella
   ```

### Emergency Fallback

If external secrets are completely unavailable:

1. **Create Manual Secrets:**
   ```bash
   # Create temporary secrets manually
   kubectl create secret generic umbrella-centralidp \
     --from-literal=admin-password=temp-password
   ```

2. **Disable External Secrets:**
   ```yaml
   external-secrets:
     enabled: false
   ```

3. **Use Legacy Configuration:**
   ```yaml
   # Revert to hardcoded values temporarily
   centralidp:
     keycloak:
       auth:
         adminPassword: "temp-password"
   ```

## Getting Help

### Log Collection

```bash
# Collect all relevant logs
kubectl logs -n external-secrets-system deployment/external-secrets > eso-logs.txt
kubectl logs -n vault vault-0 > vault-logs.txt
kubectl get events -n umbrella > events.txt
kubectl describe externalsecrets -n umbrella > externalsecrets-status.txt
```

### Support Information

When seeking support, provide:

1. **Environment Information:**
    - Kubernetes version
    - External Secrets Operator version
    - Vault version
    - Helm chart versions

2. **Configuration:**
    - Sanitized values files
    - ExternalSecret definitions
    - SecretStore configuration

3. **Logs and Status:**
    - ESO controller logs
    - Vault logs
    - ExternalSecret status
    - Kubernetes events

### Community Resources

- [External Secrets Operator Documentation](https://external-secrets.io/)
- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [Tractus-X Community](https://github.com/eclipse-tractusx)

## Prevention Best Practices

1. **Regular Monitoring:** Set up alerts for secret sync failures
2. **Backup Strategies:** Regular backups of Vault data and configurations
3. **Testing:** Regular testing of secret rotation and recovery procedures
4. **Documentation:** Keep configuration and procedures up to date
5. **Security:** Regular security audits and access reviews