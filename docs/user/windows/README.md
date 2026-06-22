# Windows Deployment Guide

This guide combines the steps for Cluster Setup, Network Setup, and Installation for Windows users.

## 1. Cluster Setup

This guide provides instructions to set up a Kubernetes cluster required for running the Umbrella Chart.

You can also follow the guide with the help of the [tutorial video](https://github.com/eclipse-tractusx/eclipse-tractusx.github.io.largefiles/blob/main/umbrella/video-tutorials/setup.mp4).

https://github.com/user-attachments/assets/c10bb246-33a1-47fa-9b94-9af433b4adfd
> [!WARNING]
> The video may not be displayed depending on your browser and browser version, try using different one if you are not able to see it.
> You can also dowload it from the previus link.

### System Requirements

| CPU (Cores) | Memory (GB) |
| :----------:| :----------:|
|      4      |      6      |

The above specifications are the minimum requirements for a local development setup. Adjust resources based on your workload for larger or production environments.

### Setup Options

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

For DNS resolution to work correctly on Windows, you have two options:

#### Option 1: Use the Hyper-V Driver

Start Minikube with administrator privileges using the `--driver=hyperv` flag:

```bash
minikube start --cpus=4 --memory=6gb --driver=hyperv
```

#### Option 2: Use Docker Desktop Kubernetes

Alternatively, you can use the native Kubernetes cluster provided by Docker Desktop:

1. Enable Kubernetes in Docker Desktop:
    - Navigate to **Settings > Kubernetes** and enable the Kubernetes option.

2. Install an NGINX Ingress Controller:

   ```bash
   helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
   ```

3. Use `127.0.0.1` as the Cluster IP and manually configure ingress.

> :warning: The rest of the tutorial assumes a minikube cluster, however.

### Windows with Ubuntu WSL

> **Note:** This guide sets up a self-contained environment within Ubuntu WSL, with no reliance on Docker Desktop or the Windows host system. The idea is to keep everything self-contained in WSL so you don’t have to touch the host system at all.

> **Tip for Docker Desktop users:** If you already have Docker Desktop installed with WSL integration enabled, you can skip the Docker installation steps — the Docker daemon should be accessible from within WSL.

Follow these steps when running Ubuntu in WSL (tested on Ubuntu 22.04/24.04):


- Install kubectl
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version
```
- Install Docker

```bash
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl status docker
> [!WARNING]
> Systemctl will only work if you have systemd enabled in your WSL. 
> Alternatively, start the service with sudo service docker start.
sudo groupadd docker
sudo usermod -aG docker $USER && newgrp docker
sudo systemctl enable docker
```

- Install cri-dockerd
```bash
wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.15/cri-dockerd_0.3.15.3-0.ubuntu-jammy_amd64.deb
sudo dpkg -i cri-dockerd_0.3.15.3-0.ubuntu-jammy_amd64.deb
```
- Install conntrack
```bash
sudo apt-get install -y conntrack
```
- Install crictl
```bash
VERSION="v1.24.2"
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
rm -f crictl-$VERSION-linux-amd64.tar.gz
```
- Install Minikube
```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin/
minikube version
```
- Install containernetworking-plugins
```bash
CNI_PLUGIN_VERSION="v1.6.0"
CNI_PLUGIN_TAR="cni-plugins-linux-amd64-$CNI_PLUGIN_VERSION.tgz"
CNI_PLUGIN_INSTALL_DIR="/opt/cni/bin"
curl -LO "https://github.com/containernetworking/plugins/releases/download/$CNI_PLUGIN_VERSION/$CNI_PLUGIN_TAR"
sudo mkdir -p "$CNI_PLUGIN_INSTALL_DIR"
sudo tar -xf "$CNI_PLUGIN_TAR" -C "$CNI_PLUGIN_INSTALL_DIR"
rm "$CNI_PLUGIN_TAR"
```
- Start Minikube and enable addons
```bash
minikube start --driver=none
kubectl get node
minikube addons enable ingress
minikube addons enable ingress-dns
```
- Install Helm
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
```
- Configure Ingress - set external IP to the minikube IP (add externalIPs below clusterIPs, as listed in the example)
```bash
kubectl get svc -n ingress-nginx
kubectl edit svc ingress-nginx-controller -n ingress-nginx
```
Example configuration:

```yaml
spec:
  clusterIP: 10.101.189.214
  clusterIPs:
  - 10.101.189.214
  externalIPs:
  - <MINIKUBE_IP>
```

### Verifying the Cluster

After starting Minikube or Docker Desktop Kubernetes, verify the cluster setup:

- Check that your cluster is running:

  ```bash
  minikube kubectl cluster-info
  ```

- Open the Minikube dashboard to monitor resources:

  ```bash
  minikube dashboard
  ```

## 2. Network Setup

This guide provides instructions to configure the network setup required for running the Umbrella Chart in a Kubernetes cluster.

### Enabled Ingresses

To enable ingress for local access, use the following command with Minikube:

```bash
minikube addons enable ingress
```

Make sure that the **DNS** resolution for the hosts is in place:

```bash
minikube addons enable ingress-dns
```

And execute installation step [3 Add the `minikube ip` as a DNS server](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns) for your OS

### Available Services

The following ingresses are configured and available:

- **Authentication Services**
  - [CentralIdP](http://centralidp.tx.test/auth/)
  - [SharedIdP](http://sharedidp.tx.test/auth/)

- **Portal Services**
  - [Portal Frontend](http://portal.tx.test)
  - [Portal Backend](http://portal-backend.tx.test)
    - [Administration API](http://portal-backend.tx.test/api/administration/swagger/index.html)
    - [Registration API](http://portal-backend.tx.test/api/registration/swagger/index.html)
    - [Apps API](http://portal-backend.tx.test/api/apps/swagger/index.html)
    - [Services API](http://portal-backend.tx.test/api/services/swagger/index.html)
    - [Notification API](http://portal-backend.tx.test/api/notification/swagger/index.html)

- **Discovery**
  - [Discovery Finder API](http://semantics.tx.test/discoveryfinder/swagger-ui/index.html)

- **Data Exchange Services**
  - [Data Consumer 1 Control Plane](http://dataconsumer-1-controlplane.tx.test)
  - [Data Consumer 1 Data Plane](http://dataconsumer-1-dataplane.tx.test)
  - [Data Provider Data Plane](http://dataprovider-dataplane.tx.test)
  - [Data Consumer 2 Control Plane](http://dataconsumer-2-controlplane.tx.test)
  - [Data Consumer 2 Data Plane](http://dataconsumer-2-dataplane.tx.test)

- **Additional Services**
  - [Business Partners Pool](http://business-partners.tx.test/pool)
  - [Business Partners Orchestrator](http://business-partners.tx.test/orchestrator)
  - [BDRS Server](http://bdrs-server.tx.test)
  - [SSI Credential Issuer](http://ssi-credential-issuer.tx.test/api/issuer/swagger/index.html)
  - [SSI DIM Wallet Stub](http://ssi-dim-wallet-stub.tx.test)
  - [pgAdmin4](http://pgadmin4.tx.test)

### DNS Resolution Setup

Proper DNS resolution is required to map local domain names to the Minikube IP address.

#### Hosts File Configuration

The following values need to be added in each case:

   ```text
   <MINIKUBE_IP>    centralidp.tx.test
   <MINIKUBE_IP>    sharedidp.tx.test
   <MINIKUBE_IP>    portal.tx.test
   <MINIKUBE_IP>    portal-backend.tx.test
   <MINIKUBE_IP>    semantics.tx.test
   <MINIKUBE_IP>    sdfactory.tx.test
   <MINIKUBE_IP>    ssi-credential-issuer.tx.test
   <MINIKUBE_IP>    dataconsumer-1-dataplane.tx.test
   <MINIKUBE_IP>    dataconsumer-1-controlplane.tx.test
   <MINIKUBE_IP>    dataprovider-dataplane.tx.test
   <MINIKUBE_IP>    dataprovider-controlplane.tx.test
   <MINIKUBE_IP>    dataprovider-submodelserver.tx.test
   <MINIKUBE_IP>    dataconsumer-2-dataplane.tx.test
   <MINIKUBE_IP>    dataconsumer-2-controlplane.tx.test
   <MINIKUBE_IP>    bdrs-server.tx.test
   <MINIKUBE_IP>    business-partners.tx.test
   <MINIKUBE_IP>    pgadmin4.tx.test
   <MINIKUBE_IP>    ssi-dim-wallet-stub.tx.test
   <MINIKUBE_IP>    smtp.tx.test
   ```

##### Windows

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

   1. Open the hosts file you find here: `C:\Windows\System32\drivers\etc\hosts` and insert the values from above.

   2. Replace `<MINIKUBE_IP>` with the output of the following command:

      ```bash
         minikube ip
      ```

   3. Test DNS resolution by pinging one of the configured hostnames.

#### Alternative approaches

##### Windows alternative

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

1. Open PowerShell as Administrator.
2. Add a DNS client rule for `.test` domains:

   ```bash
   Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

   The following will remove any matching rules before creating a new one. This is useful for updating the minikube ip.

   ```shell
   Get-DnsClientNrptRule | Where-Object {$_.Namespace -eq '.test'} | Remove-DnsClientNrptRule -Force; Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

3. Test DNS resolution by pinging one of the configured hostnames.

### Verify Network Setup

Once the DNS resolution or hosts file is configured:

1. Ensure ingress is working by accessing a service endpoint, such as <http://portal.tx.test>

### Troubleshooting

For common issues and solutions, please refer to the [Troubleshooting Guide](../common/troubleshooting/README.md).

## 3. Installation

# Install from local repository

Make sure to clone the [tractus-x-umbrella](https://github.com/eclipse-tractusx/tractus-x-umbrella) repository beforehand.

Update the chart dependencies of the umbrella helm chart and their dependencies.
```bash
helm dependency update charts/data-persistence-layer-bundle
helm dependency update charts/dataspace-connector-bundle
helm dependency update charts/digital-twin-bundle
helm dependency update charts/identity-and-trust-bundle
helm dependency update charts/tx-data-provider
helm dependency update charts/umbrella
```

Navigate to the `charts/umbrella` directory.
```bash
cd charts/umbrella/
```

**:grey_question: Command explanation**

> `helm install` is used to install a Helm chart.
> > `-f your-values.yaml` | `-f values-*.yaml` specifies the values file to use for configuration.
>
> > `umbrella` is the release name for the Helm chart.
>
> > `.` specifies the path to the chart directory.
>
> > `--namespace umbrella` specifies the namespace in which to install the chart.
>
> > `--create-namespace` create a namespace with the name `umbrella`.

### Custom Configuration

Install your chosen components by having them enabled in a `your-values.yaml` file:

```bash
helm install -f your-values.yaml umbrella . --namespace umbrella --create-namespace
```

> In general, all your specific configuration and secret values should be set by installing with an own values file.

Choose to install one of the predefined subsets (currently in focus of the **E2E Adopter Journey**):

### Data Exchange Subset

The Data Exchange subset enables secure data sharing between participants in the network.

```bash
helm install -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella --create-namespace
```

#### Enable Additional Data Consumers

To enable an additional data consumer (`dataconsumerTwo`), follow these steps:

1. Update the `values-adopter-data-exchange.yaml` file to set `dataconsumerTwo` as enabled:
   ```yaml
   dataconsumerTwo:
     enabled: true
   ```

2. Apply the changes by upgrading the Helm release:
   ```bash
   helm upgrade -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella
   ```

### Portal Subset

The Portal subset provides a user-friendly interface for participant onboarding and management.

```bash
helm install -f values-adopter-portal.yaml umbrella . --namespace umbrella --create-namespace
```

## Next Steps

After successfully deploying the Umbrella Chart, you can explore the following guides to continue your journey:

- **Guides**:
  - [Data Exchange Guide](../common/guides/data-exchange.md) - Learn how to provide and consume data.
  - [Portal Usage Guide](../common/guides/portal-usage.md) - Instructions on how to use the Portal.
  - [Database Access](../common/guides/database-access.md) - How to access the databases.
  - [Observability](../common/guides/observability/observability.md) - Monitoring and logging.
  - [Hausanschluss Bundles](../common/guides/hausanschluss-bundles.md) - Information about Hausanschluss bundles.
  - [External Secrets](../common/guides/external-secrets.md) - Managing external secrets.

- **Secrets Management**:
  - [Secrets Overview](../common/secrets/README.md) - Comprehensive guide on secrets management.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
