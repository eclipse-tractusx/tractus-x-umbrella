# Identity and Trust Bundle

![Version: 1.1.2](https://img.shields.io/badge/Version-1.1.2-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

Helm chart for Capability Bundle: Identity and Trust

The Identity & Trust Bundle provides identity management and authentication services for the Catena-X ecosystem.

For more information on the SSI DIM Wallet stub application, see https://github.com/eclipse-tractusx/ssi-dim-wallet-stub

**Homepage:** <https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/identity-and-trust-bundle>

### Launching the application

Run this shell command to start the Capability Bundle: Identity and Trust:

```shell
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm install my-release tractusx-dev/identity-and-trust-bundle
```

## Source Code

* <https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/identity-and-trust-bundle>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://eclipse-tractusx.github.io/charts/dev | ssi-dim-wallet-stub | 0.1.14 |

## Values

### Wallet Component Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.enabled | bool | `true` | Enable SSI DIM Wallet deployment |
| ssi-dim-wallet-stub.wallet.nameSpace | string | `"default"` | Kubernetes namespace |

### Wallet Core Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.wallet.baseWalletBpn | string | `"BPNL00000003CRHK"` | Operator BPN |
| ssi-dim-wallet-stub.wallet.statusListVcId | string | `"8a6c7486-1e1f-4555-bdd2-1a178182651e"` | Default status list VC id |
| ssi-dim-wallet-stub.wallet.stubUrl | string | `"http://ssi-dim-wallet-stub.tx.test"` | Wallet stub server URL. This will pe part of the presentation query API in the did document |
| ssi-dim-wallet-stub.wallet.tokenExpiryTime | string | `"5"` | Token expiry time in seconds |

### Wallet Ingress Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.wallet.didHost | string | `"ssi-dim-wallet-stub.tx.test"` | Did document host, this will be part of did String i.e., did:web:<didHost> |
| ssi-dim-wallet-stub.wallet.host | string | `"ssi-dim-wallet-stub.tx.test"` | External hostname for wallet |
| ssi-dim-wallet-stub.wallet.ingress.enabled | bool | `true` | Enable ingress creation |
| ssi-dim-wallet-stub.wallet.ingress.tls.enabled | bool | `false` | Enable TLS |
| ssi-dim-wallet-stub.wallet.ingress.tls.name | string | `""` | TLS secret name |
| ssi-dim-wallet-stub.wallet.ingress.urlPrefix | string | `"/"` | URL prefix |

### (Optional) Keycloak Integration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.wallet.keycloak.authServerUrl | string | `"http://centralidp.tx.test/auth"` | Keycloak auth server URL |
| ssi-dim-wallet-stub.wallet.keycloak.realm | string | `"CX-Central"` | Keycloak realm name |

### (Optional) Portal Integration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.wallet.portal.clientId | string | `"sa-cl2-05"` | Keycloak client_id. We will create an access token and using this we access portal backend APIs |
| ssi-dim-wallet-stub.wallet.portal.clientSecret | Optional | `"changeme"` | Keycloak client_secret. We will create an access token and using this we access portal backend APIs |
| ssi-dim-wallet-stub.wallet.portal.host | string | `"http://portal-backend.tx.test"` | Portal backend application host |
| ssi-dim-wallet-stub.wallet.portal.waitTime | string | `"60"` | Wait for given seconds before pushing data to portal backend after wallet creation |

### Wallet Seeding Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.wallet.seeding.bpnList | string | `"BPNL00000003AZQP,BPNL00000003AYRE"` | List of BPNs for which wallets will be seeded on application startup |

### Other Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ssi-dim-wallet-stub.postgresql.auth.password | string | `"postgrespassword"` |  |
| ssi-dim-wallet-stub.postgresql.auth.username | string | `"postgres"` |  |
| ssi-dim-wallet-stub.postgresql.configmap.name | string | `"wallet-postgres-configmap"` |  |
| ssi-dim-wallet-stub.postgresql.enabled | bool | `true` |  |
| ssi-dim-wallet-stub.postgresql.fullnameOverride | string | `"wallet-postgres"` |  |
| ssi-dim-wallet-stub.postgresql.persistence.enabled | bool | `false` |  |
| ssi-dim-wallet-stub.postgresql.persistence.size | string | `"10Gi"` |  |
| ssi-dim-wallet-stub.postgresql.persistence.storageClass | string | `"standard"` |  |
| ssi-dim-wallet-stub.wallet.livenessProbe | object | `{"enabled":true,"failureThreshold":3,"initialDelaySeconds":75,"periodSeconds":15,"timeoutSeconds":60}` | Kubernetes [liveness-probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) |
| ssi-dim-wallet-stub.wallet.livenessProbe.enabled | bool | `true` | Enables/Disables the livenessProbe at all |
| ssi-dim-wallet-stub.wallet.livenessProbe.failureThreshold | int | `3` | When a probe fails, Kubernetes will try failureThreshold times before giving up. Giving up in case of liveness probe means restarting the container. |
| ssi-dim-wallet-stub.wallet.livenessProbe.initialDelaySeconds | int | `75` | Number of seconds after the container has started before readiness probes are initiated. |
| ssi-dim-wallet-stub.wallet.livenessProbe.periodSeconds | int | `15` | How often (in seconds) to perform the probe |
| ssi-dim-wallet-stub.wallet.livenessProbe.timeoutSeconds | int | `60` | Number of seconds after which the probe times out. |
| ssi-dim-wallet-stub.wallet.postgresql.password | string | `"postgrespassword"` |  |
| ssi-dim-wallet-stub.wallet.postgresql.username | string | `"postgres"` |  |
| ssi-dim-wallet-stub.wallet.readinessProbe | object | `{"enabled":true,"failureThreshold":3,"initialDelaySeconds":75,"periodSeconds":15,"successThreshold":1,"timeoutSeconds":60}` | Kubernetes [readiness-probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) |
| ssi-dim-wallet-stub.wallet.readinessProbe.enabled | bool | `true` | Enables/Disables the readinessProbe at all |
| ssi-dim-wallet-stub.wallet.readinessProbe.failureThreshold | int | `3` | When a probe fails, Kubernetes will try failureThreshold times before giving up. In case of readiness probe the Pod will be marked Unready. |
| ssi-dim-wallet-stub.wallet.readinessProbe.initialDelaySeconds | int | `75` | Number of seconds after the container has started before readiness probe are initiated. |
| ssi-dim-wallet-stub.wallet.readinessProbe.periodSeconds | int | `15` | How often (in seconds) to perform the probe |
| ssi-dim-wallet-stub.wallet.readinessProbe.successThreshold | int | `1` | Minimum consecutive successes for the probe to be considered successful after having failed. |
| ssi-dim-wallet-stub.wallet.readinessProbe.timeoutSeconds | int | `60` | Number of seconds after which the probe times out. |
| ssi-dim-wallet-stub.wallet.resources.limits.cpu | int | `1` | CPU resource limits |
| ssi-dim-wallet-stub.wallet.resources.limits.memory | string | `"2Gi"` | Memory resource limits |
| ssi-dim-wallet-stub.wallet.resources.requests.cpu | string | `"500m"` | CPU resource requests |
| ssi-dim-wallet-stub.wallet.resources.requests.memory | string | `"1Gi"` | Memory resource requests |
| ssi-dim-wallet-stub.wallet.service.port | int | `8080` |  |
| ssi-dim-wallet-stub.wallet.service.type | string | `"ClusterIP"` |  |

## Contributing

Contributions are welcome! Please see our [Contributing Guide](/CONTRIBUTING.md) for details.

----------------------------------------------
Autogenerated from chart metadata using [helm-docs](https://github.com/norwoodj/helm-docs/) 
Generate this document by running `helm-docs -s file` in this folder
