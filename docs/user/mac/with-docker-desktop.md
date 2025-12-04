# macOS Deployment Guide (with Docker Desktop)

This guide combines the steps for Cluster Setup, Network Setup, and Installation for macOS users using Docker Desktop and Minikube.

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

### Enable Ingress

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

##### macOS using minikube

   1. Open the hosts file you find here: `/etc/hosts` and insert the values from above.

   2. Replace `<MINIKUBE_IP>` with the output of the following command:

      ```bash
         minikube ip
      ```

   3. Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

      We recommend to execute the usage example that can be found there after installation to check proper setup.

   4. Test DNS resolution by pinging one of the configured hostnames.

#### Alternative approaches

##### macOS using Minikube

Please refer to the following instructions for the dns setup in case you're using Minikube, which is the most tested and therefore the recommended option.

1. Create a resolver configuration for `.test` domains:

   ```bash
   sudo mkdir -p /etc/resolver
   sudo bash -c "echo 'nameserver $(minikube ip)' > /etc/resolver/test"
   ```

   and also add these lines to `/etc/resolver/test`:

   ```bash
   domain tx.test
   search_order 1
   timeout 5
   ```

2. Additional network setup for macOS

   Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

   We recommend to execute the usage example that can be found there after installation to check proper setup.

3. Test DNS resolution by pinging one of the configured hostnames.

### Verify Network Setup

Once the DNS resolution or hosts file is configured:

1. Ensure ingress is working by accessing a service endpoint, such as <http://portal.tx.test>

### Troubleshooting

#### DNS resolution fails due to resolution timeouts

**Problem background**

Minikube node DNS settings are inherited from the configuration specified in the `/etc/resolv.conf` file on the host where Minikube is running. This particularly applies to the search field in the `resolv.conf` file.
The values defined in the search field are propagated to individual pods within the cluster. 

The search field contains a list of domain suffixes that are appended to queried domain names. 
These modified domain names are then sequentially resolved by the DNS server.

In certain circumstances, this mechanism can lead to issues such as domain name resolution timeouts.

**Problem symptoms**

- umbrella-dataprovider-post-install-testdata-...  pod fails
- It is not possible to query DSP catalog because of the HTTP 500 ERROR. 
- When looking into umbrella-dataconsumer-1-edc-controlplane logs, there are this kind of error messages:

   ```text
   HTTP client exception caught for request [POST, http://ssi-dim-wallet-stub.tx.test/oauth/token]
   org.eclipse.edc.http.spi.EdcHttpClientException: ssi-dim-wallet-stub.tx.test: Try again
   ```

- There are some timeout errors related to domain names resolution in CoreDns log:

   ```text
   [ERROR] plugin/errors: 2 ssi-dim-wallet-stub.tx.test.some-domain.com. A: read udp 10.244.1.154:36890->8.8.8.8:53: i/o timeout
   [ERROR] plugin/errors: 2 ssi-dim-wallet-stub.tx.test.some-domain.com. AAAA: read udp 10.244.1.154:35576->8.8.8.8:53: i/o timeout
   ```

- When trying to ping any domain from inside any pod in the cluster, domain name resolution fails or gets timeout. Adding a dot (for example `google.com.`) at the end of the domain fixes the issue.

**Solution**

Prevent pods from inheriting `/etc/resolv.conf` search field values from the Minikube node.

1. Log into Minikube node, using `ssh`.

   ```bash
   minikube ssh
   ```

   In the Minikube node, install any text editor, for example vim:

   ```bash
   sudo apt update && apt install vim
   ```
 
2. While still in the Minikube node console, duplicate existing `/etc/resolv.conf` file, for example:

   ```shell
   cp /etc/resolv.conf  /etc/umbrella.resolv.conf
   ```

3. Using `vim`, `nano` or any other text editor, open the `/etc/umbrella.resolv.conf` file and **comment out the "search"** line. Save the file. Exit Minikube console.

   ```shell
   vim /etc/umbrella.resolv.conf
   exit
   ```

4. Stop the Minikube and start it again appending the following flag to Minikube startup command:
   
   ```text
   --extra-config=kubelet.resolv-conf="/etc/umbrella.resolv.conf"
   ```
      
   So the final Minikube startup command will look like this:

   ```shell
   minikube start --cpus=4 --memory=6gb --extra-config=kubelet.resolv-conf="/etc/umbrella.resolv.conf"
   ```

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
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
