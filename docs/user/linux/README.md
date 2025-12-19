# Linux Deployment Guide

This guide combines the steps for Cluster Setup, Network Setup, and Installation for Linux users.

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

### Start Minikube

Start a Minikube cluster with the following command:

```bash
minikube start --cpus=4 --memory=6gb
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

1. Open the hosts file you find here `/etc/hosts` and insert the values from below.

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

2. Replace `<MINIKUBE_IP>` with the output of the following command:

   ```bash
      minikube ip
   ```

3. Test DNS resolution by pinging one of the configured hostnames.

#### Alternative approaches

1. Identify your DNS resolver by checking the contents of `/etc/resolv.conf`.
2. Update the resolver configuration based on your system:

    - **resolvconf**:
      Add the following to `/etc/resolvconf/resolv.conf.d/base`:

      ```bash
      search test
      nameserver $(minikube ip)
      timeout 5
      ```

      If your Linux OS uses `systemctl`, run the following commands:

      ```bash
      sudo resolvconf -u
      systemctl disable --now resolvconf.service
      ```

      See <https://linux.die.net/man/5/resolver> for more information.

    - **NetworkManager**:
      NetworkManager can run integrated caching DNS server - `dnsmasq` plugin and can be configured to use separate nameservers per domain.

      Edit `/etc/NetworkManager/NetworkManager.conf` and enable `dns=dnsmasq` by adding:

      ```bash
      [main]
      dns=dnsmasq
      ```

      Also see `dns=` in [NetworkManager.conf](https://developer.gnome.org/NetworkManager/stable/NetworkManager.conf.html).

      Configure dnsmasq to handle domain names ending with `.test`:

      ```bash
      sudo mkdir -p /etc/NetworkManager/dnsmasq.d/
      echo "server=/test/$(minikube ip)" | sudo tee /etc/NetworkManager/dnsmasq.d/minikube.conf
      ```

      Restart NetworkManager:

      ```bash
      systemctl restart NetworkManager.service
      ```

      Ensure your `/etc/resolv.conf` contains only single nameserver:

      ```bash
      cat /etc/resolv.conf | grep nameserver
      nameserver 127.0.0.1
      ```

    - **systemd-resolved**:
      Run the following commands to add the minikube DNS for `.test` domains:

      ```bash
      sudo mkdir -p /etc/systemd/resolved.conf.d
      sudo tee /etc/systemd/resolved.conf.d/minikube.conf << EOF
      [Resolve]
      DNS=$(minikube ip)
      Domains=~test
      EOF
      sudo systemctl restart systemd-resolved
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
