# External Secrets Operator

This guide explains how to use the External Secrets Operator with the Umbrella Chart.

## Overview

The [External Secrets Operator](https://external-secrets.io/) is a Kubernetes operator that integrates external secret management systems like AWS Secrets Manager, HashiCorp Vault, Google Secret Manager, and others with Kubernetes. It allows you to securely manage secrets outside of your Kubernetes cluster and use them in your applications.

The Umbrella Chart includes the External Secrets Operator as an auxiliary component, which can be enabled and configured as needed.

## Configuration

### Enabling the External Secrets Operator

To enable the External Secrets Operator, set the `external-secrets.enabled` value to `true` in your values file:

```yaml
external-secrets:
  enabled: true
```

### Example Configuration

The Umbrella Chart includes an example configuration for the External Secrets Operator that demonstrates how to use it with the filesystem provider. This example configuration:

1. Creates a ConfigMap that contains your secrets.json content
2. Creates a SecretStore that uses the file provider
3. Creates an ExternalSecret that references the SecretStore
4. Maps keys from the source secret to keys in the target secret

#### Configuration in values.yaml

```yaml
external-secrets:
  enabled: true
  installCRDs: true
  webhook:
    create: true
  certController:
    enabled: true
  # Configure the filesystem provider
  extraVolumes:
    - name: secrets-volume
      configMap:
        name: test-secrets-configmap
  extraVolumeMounts:
    - name: secrets-volume
      mountPath: /secrets
      readOnly: true
```

#### Template Files

The Umbrella Chart includes the following template files for the External Secrets Operator:

1. **ConfigMap Template** (`charts/umbrella/templates/test-secrets-configmap.yaml`):
```
# {{- if (index .Values "external-secrets" "enabled") }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-secrets-configmap
data:
  secrets.json: |
    # {{ .Files.Get "secrets/secrets.json" | indent 4 }}
# {{- end }}
```

2. **SecretStore Template** (`charts/umbrella/templates/test-secretstore.yaml`):
```
# {{- if (index .Values "external-secrets" "enabled") }}
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: file-secretstore
spec:
  provider:
    filesystem:
      mountPath: "/secrets"
# {{- end }}
```

3. **ExternalSecret Template** (`charts/umbrella/templates/test-externalsecret.yaml`):
```
# {{- if (index .Values "external-secrets" "enabled") }}
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: test-external-secret
spec:
  refreshInterval: "1m"
  secretStoreRef:
    name: file-secretstore
    kind: SecretStore
  target:
    name: example-secret
  data:
  - secretKey: username
    remoteRef:
      key: secrets.json
      property: username
  - secretKey: password
    remoteRef:
      key: secrets.json
      property: password
# {{- end }}
```

### Example Secret

The Umbrella Chart includes an example secrets file (`charts/umbrella/secrets/secrets.json`) that contains a simple JSON object with username and password fields:

```json
{
  "username": "test-user",
  "password": "test-password"
}
```

This file is automatically included in the ConfigMap created by the template, so you don't need to create it separately.

## Using External Secrets in Your Applications

Once the External Secrets Operator is enabled and configured, you can use the secrets in your applications by referencing the target Secret created by the ExternalSecret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
spec:
  containers:
  - name: example-container
    image: example-image
    env:
    - name: USERNAME
      valueFrom:
        secretKeyRef:
          name: example-secret
          key: username
    - name: PASSWORD
      valueFrom:
        secretKeyRef:
          name: example-secret
          key: password
```

## Testing the Implementation

The Umbrella Chart includes a test pod that verifies the external secret is properly created and can be accessed. This pod is created as a post-install hook and will output the secret value to confirm it's working correctly:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-external-secret
  annotations:
    helm.sh/hook: post-install,post-upgrade
    helm.sh/hook-weight: "0"
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
spec:
  containers:
  - name: test-container
    image: busybox:latest
    command: ['sh', '-c', 'echo "Testing external secret access" && echo "Secret value: $SECRET_VALUE" && echo "Test completed successfully"']
    env:
    - name: SECRET_VALUE
      valueFrom:
        secretKeyRef:
          name: example-secret
          key: password
  restartPolicy: Never
```

You can check the logs of this pod to verify that the secret was successfully created and accessed:

```bash
kubectl logs test-external-secret -n <namespace>
```

The output should include the message "Secret value: test-password" if everything is working correctly.

## Advanced Configuration

For more advanced configuration options, refer to the [External Secrets Operator documentation](https://external-secrets.io/latest/).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>