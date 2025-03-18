# Quickinstall Guide for a Basic installation


This guide helps you deploy a minimal version of the Tractus-X Umbrella chart focused on the following services:
- [centralidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.0.1)
- [sharedidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.0.1)
- [portal](https://github.com/eclipse-tractusx/portal/tree/portal-2.3.0)
- [ssi-dim-wallet-stub](https://github.com/eclipse-tractusx/ssi-dim-wallet-stub/releases/tag/ssi-dim-wallet-stub-0.1.2)
- [tx-data-provider](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.7.1), [digital-twin-registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/digital-twin-registry-0.6.3), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0), [simple-data-backend](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/simple-data-backend))

>[!note]
>
> For comprehensive guides, visit the [Tractus-X Umbrella documentation](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/user)

## Cluster Setup

### Prerequisites

1. A system with at least:
- 4 CPU cores
- 16GB RAM
- 20GB storage

2. Required tools:
- kubectl (Installation [kubernetes.io](https://kubernetes.io/docs/tasks/tools/#kubectl))
- Helm v3.8+ (Installation [helm.sh](https://helm.sh/docs/intro/install/))
- Minikube (Installation [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)) *preferred*

### 1. Set Up Minikube (for local development)

>[!note]
> **[MacOS Only]** In case Docker Desktop isn't available, follow this guide: https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/user/setup#option-1-docker-desktop-available
>
> If you follow the guide above ignore all minikube related commands

#### Linux Set Up

Start Minikube with sufficient resources:

```bash
minikube start --cpus=4 --memory=8Gb
```

#### Windows Set Up

For windows the easy way is to enable Kubernetes in Docker Desktop:

1. Enable Kubernetes in Docker Desktop:
- Navigate to Settings > Kubernetes and enable the Kubernetes option.

2. Install an NGINX Ingress Controller:
```sh
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```
Use 127.0.0.1 as the Cluster IP and manually configure ingress.

>[!important]
> If you follow the windows guide, ignore all minikube commands

>[!warning]
> The Windows setup isn't extensively tested, and you may encounter issues. We would appreciate any contributions from those who successfully deploy it on Windows.

#### Verifying the Cluster
After starting Minikube or Docker Desktop Kubernetes, verify the cluster setup.

Check that your cluster is running:
```bash
kubectl cluster-info
```

Enable the minikube dashboard addon:
```bash
minikube addons enable dashboard
```

Open the Minikube dashboard to monitor your kubernetes resources:
```bash
minikube dashboard
```

### 2. Enable Ingress Controller (Minikube Only)

```bash
minikube addons enable ingress
minikube addons enable ingress-dns
```

### 3. Get Minikube IP

```bash
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"
```

### 4. Configure DNS

Add these entries to your `/etc/hosts` file (replace **192.168.49.2** with your Minikube IP, 192.168.49.2 is the default Minikube IP. Replace with **127.0.0.1** if you are using Docker Desktop with ingress-nginx controller):

```bash
# Add to /etc/hosts
192.168.49.2 centralidp.tx.test
192.168.49.2 sharedidp.tx.test
192.168.49.2 portal.tx.test
192.168.49.2 portal-backend.tx.test
192.168.49.2 dataprovider.tx.test
192.168.49.2 dataprovider-controlplane.tx.test
192.168.49.2 dataprovider-dataplane.tx.test
192.168.49.2 dataprovider-dtr.tx.test
192.168.49.2 dataprovider-submodelserver.tx.test
192.168.49.2 ssi-dim-wallet-stub.tx.test
192.168.49.2 pgadmin4.tx.test
```

>[!note]
> If you wish more advanced configurations, please refer to the documentation available at: https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/user/network

## Deployment

### 1. 

<details>
    <summary>
        Copy the code and create a {your-name}.yaml file on your local system
    </summary>

```yaml
###############################################################
# Eclipse Tractus-X - Industry Core Hub
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
###############################################################
portal:
  enabled: true
  # -- uncomment the following for persistance
  # postgresql:
  #   primary:
  #     persistence:
  #       enabled: true

centralidp:
  enabled: true
  # -- uncomment the following for persistance
  # keycloak:
  #   postgresql:
  #     primary:
  #       persistence:
  #         enabled: true

sharedidp:
  enabled: true
  # -- uncomment the following for persistance
  # keycloak:
  #   postgresql:
  #     primary:
  #       persistence:
  #         enabled: true

tx-data-provider:
  enabled: true
  seedTestdata: true
  # -- uncomment the following for persistance
  # postgresql:
  #   primary:
  #     persistence:
  #       enabled: true
  digital-twin-registry:
    registry:
      host: dataprovider-dtr.tx.test
      ingress:
        enabled: true
        urlPrefix: /

ssi-dim-wallet-stub:
  enabled: true

pgadmin4:
  enabled: true
  # -- uncomment the following for persistance
  # persistentVolume:
  #   enabled: true
```
</details>


The Helm chart configuration for Tractus-X Umbrella is complex and contains hundreds of values across multiple files. The values we are using, only overrides specific values from the main `values.yaml` file in the Umbrella chart repository.

> **Important**: Only developers familiar with Helm charts and the Tractus-X architecture should modify the values beyond what's provided in this guide. Incorrect configurations can lead to non-functional deployments or security issues.

The base values can be found in the [umbrella chart's values.yaml file](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/umbrella-2.6.0/charts/umbrella/values.yaml). Our `values.yaml` follows a similar structure as the `values-adopter-portal.yaml` file but focuses on only the essential services.

### 2. Install the Chart

Assuming you are in the root folder of the project, run these commands. If you're working from a different directory, adjust the path to the minimal-values.yaml file accordingly.

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm repo update tractusx-dev
```

**Replace** path/to/file/{your-name}.yaml with the above created yaml file:
```bash
helm install -f path/to/file/{your-name}.yaml umbrella tractusx-dev/umbrella --namespace umbrella --version v2.6.0 --create-namespace
```

If you modify any value in the `{your-name}.yaml` you can upgrade the deployment running
```bash
helm upgrade -f path/to/file/{your-name}.yaml umbrella tractusx-dev/umbrella --namespace umbrella --version v2.6.0
```

>[!important]
>Once the installation or upgrade is succesfull run this patch
>```bash
>kubectl patch ingress umbrella-dataprovider-dtr \
>  --type='json' \
>  -p='[{"op": "replace", "path": "/spec/rules/0/http/paths/0/path", "value": "/"}]' \
>  -n umbrella
>```
>
> This patch modifies the Digital Twin Registry (DTR) ingress path to use a simple root path ("/") instead of the more complex URL pattern defined in the template. This patch is necessary due to not overridable configuration in the DTR chart. While the technical details involve how the ingress controller processes URL patterns, the important part is that this patch ensures the DTR API endpoints are properly accessible at the expected URL.

### 3. Check Deployment Status

```bash
kubectl get pods -n umbrella
```

Wait until all pods are in the Running state. This may take several minutes for the first deployment.

```bash
# You can watch the pod status
kubectl get pods -n umbrella -w
```

### 4. Check Service Access

Verify that the ingress resources are properly created:

```bash
kubectl get ingress -n umbrella
```

## Enabling Persistence

By default, the minimal configuration uses ephemeral storage, which means all data will be lost when pods are restarted. For a more robust setup, you can enable persistence.

### 1. Configure Storage Class

For Minikube, enable the default storage provisioner:

```bash
# For Minikube
minikube addons enable storage-provisioner
kubectl get storageclass
```

For other environments, ensure you have a storage class available:

```bash
# Check available storage classes
kubectl get storageclass
```

### 2. Enable Persistence in Values File

The path/to/file/{your-name}.yaml file above already includes persistence configuration that is commented out. To enable persistence, simply uncomment the persistence sections for the components you want to persist in the [Custom Values File](./README.md#deployment).

- Uncomment these sections for the desired components:
    - Portal PostgreSQL
    - CentralIDP PostgreSQL
    - SharedIDP PostgreSQL
    - Data Provider PostgreSQL
    - PGAdmin4

For example, to enable persistence **(in your local copy)** for the Portal's database, uncomment these lines:

```yaml
# Before:
# persistence:
#   enabled: true

# After uncommenting:
persistence:
  enabled: true
```

### 3. Apply Changes

After uncommenting the persistence configurations, upgrade your Helm deployment:

```bash
helm upgrade -f path/to/file/{your-name}.yaml umbrella tractusx-dev/umbrella --namespace umbrella --version v2.6.0
```

### 4. Verify Persistent Volumes

Confirm that PersistentVolumeClaims (PVCs) have been created and bound:

```bash
kubectl get pvc -n umbrella
```

>[!note]
> Enabling persistence will increase resource requirements. Ensure your cluster has sufficient storage capacity.

## Default Credentials

### CentralIDP (Keycloak)

- URL: http://centralidp.tx.test/auth/
- Username: `admin`
- Password: `adminconsolepwcentralidp`

### SharedIDP (Keycloak)

- URL: http://sharedidp.tx.test/auth/
- Username: `admin`
- Password: `adminconsolepwsharedidp`

### Portal

- URL: http://portal.tx.test/
- Username: `cx-operator@tx.test`
- Password: `tractusx-umbr3lla!`

### PGAdmin4

- URL: http://pgadmin4.tx.test
- Username: `pgadmin4@txtest.org`
- Password: `tractusxpgadmin4`

#### Database Connection Details

For all connections:
- Username: `postgres`
- Port: `5432`

| Component         | Host                              |Password                   |
|-------------------|-----------------------------------|---------------------------|
| Portal            | `umbrella-portal-backend-postgresql` |`dbpasswordportal`         |
| CentralIdP        | `umbrella-centralidp-postgresql`    |`dbpasswordcentralidp`     |
| SharedIdP         | `umbrella-sharedidp-postgresql`    |`dbpasswordsharedidp`      |
| MIW               | `umbrella-miw-postgres`            |`dbpasswordmiw`            |
| Data Provider     | `umbrella-dataprovider-db`         |`dbpasswordtxdataprovider` |

#### Verifying Database Access

To verify access, follow these steps:

1. Open pgAdmin4.
2. Add a new server connection for the desired database.
3. Test the connection by browsing schemas and running queries.

## Interacting with Services

### 1. CentralIDP

The CentralIDP is a Keycloak instance that serves as the central identity provider:

1. Access the admin console at http://centralidp.tx.test/auth/admin/
2. Login with the admin credentials
3. You can manage clients, users, and realms for the Catena-X ecosystem

Key features:
- Client management for all Catena-X services
- User federation
- Role and permission management

### 2. SharedIDP

The SharedIDP is another Keycloak instance for company-specific identities:

1. Access the admin console at http://sharedidp.tx.test/auth/admin/
2. Login with the admin credentials
3. This IDP is used by applications like the portal and dataprovider

Key features:
- Manages company-specific user identities
- Federation with CentralIDP
- Used by Portal and other applications for user authentication

### 3. Portal

The Portal is the main entry point for Catena-X applications:

1. Access the portal at http://portal.tx.test/
2. Login with the cx-operator user
3. From here you can access registered apps and manage users

Key features:
- App Marketplace for Catena-X applications
- User and company management
- Service subscription and management

### 4. Dataprovider and Related Components

The Dataprovider deployment includes several integrated components that enable data exchange and digital twin functionality:

#### 4.1 Dataprovider EDC Connectors
- Data sharing and exchange functionality through Eclipse Dataspace Connector (EDC)
- API endpoints for data assets and contract negotiation
- Consists of both control plane and data plane components
- Control plane URL: http://dataprovider-controlplane.tx.test/
- Data plane URL: http://dataprovider-dataplane.tx.test/

#### 4.2 Digital Twin Registry
- Allows registration and discovery of digital twins
- Provides APIs for managing digital twin metadata
- Digital Twin Registry URL: http://dataprovider-dtr.tx.test/

#### 4.3 Submodel Server
- Hosts the actual data models and assets
- Provides standardized APIs for accessing submodel data
- Submodel server URL: http://dataprovider-submodelserver.tx.test/

These components work together to enable the complete data exchange and digital twin capabilities required for Catena-X use cases.

### 6. PGAdmin4

PGAdmin4 is a web-based administration tool for PostgreSQL databases:

1. Access the web UI at http://pgadmin4.tx.test
2. Login using the admin credentials
3. To connect to a database:
    - Right-click on "Servers" and select "Create" → "Server..."
    - Name: Give a descriptive name (e.g., "Portal DB")
    - Connection tab:
        - Host: Use the service name of the database (e.g., `umbrella-portal-backend-postgresql`)
        - Port: 5432
        - Maintenance database: postgres
        - Username: postgres
        - Password: Use the password defined in [Database Connection Details](./README.md#database-connection-details) (e.g., "dbpasswordportal")


## Troubleshooting

### Common Issues

1. **Ingress not working**:
- Verify that your `/etc/hosts` file is correctly configured with the Minikube IP
- Check if the Minikube ingress addon is enabled: `minikube addons list`
- Ensure your Minikube IP is correct: `minikube ip`

2. **Pods not starting**:
```bash
kubectl describe pod <pod-name> -n umbrella
```

3. **Service connectivity issues**:
```bash
kubectl get ingress -n umbrella
```

4. **Resource constraints**:
   If pods are stuck in Pending state, check if you have enough resources:
```bash
kubectl describe nodes
```

5. **Log inspection**:
```bash
kubectl logs <pod-name> -n umbrella
```

### Specific Service Issues

1. **CentralIDP/SharedIDP Keycloak Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=centralidp -n umbrella
kubectl logs -l app.kubernetes.io/name=sharedidp -n umbrella
```

2. **Portal Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=portal -n umbrella
```

3. **Dataprovider Issues**:
```bash
kubectl logs -l app.kubernetes.io/name=dataprovider-edc-controlplane -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-edc-dataplane -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-dtr -n umbrella
kubectl logs -l app.kubernetes.io/name=dataprovider-submodelserver -n umbrella
```

## Cleanup

To remove the deployment:

```bash
helm uninstall umbrella -n umbrella
kubectl delete namespace umbrella
```

To stop the cluster:
```bash
minikube stop
```

To restart the cluster:
```bash
minikube start
```

To delete the cluster:
```bash
minikube delete
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/industry-core-hub>