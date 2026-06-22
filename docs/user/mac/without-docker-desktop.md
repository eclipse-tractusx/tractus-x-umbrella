# macOS Deployment Guide (without Docker Desktop)

This guide combines the steps for Cluster Setup, Network Setup, and Installation for macOS users using Lima and K3s.

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

In this case, a tested way to setup your local kubernetes cluster is with [lima](https://lima-vm.io/) and [K3s](https://k3s.io/):

```bash
brew install lima

#as we are using a vm template, we download it first
curl -O https://raw.githubusercontent.com/lima-vm/lima/refs/heads/master/templates/k3s.yaml
```

then we need to modify it a little, to propagate your proxysettings, add the following:

```yaml
propagateProxyEnv: true
```

if you for example need ca-certificates because of a corporate proxy then add the following:

```yaml
caCerts:
  removeDefaults: null
  files:
  - /path/to/your/certificates/ca-certificates.crt
```

to adjust the size of your vm add:

```yaml
cpus: 6
memory: 8GiB
```

to support also non-arm images in your cluster add:

```yaml
rosetta:
  enabled: true
  binfmt: true
vmType: vz
```

as K3s comes with traefik by default and these helm charts are for NGINX ingress, we need to modify the install script (starting line 39) a [little](https://www.suse.com/support/kb/doc/?id=000020082):

```yaml
- mode: system
  script: |
    #!/bin/bash
    set -eux -o pipefail
    export K3S_KUBECONFIG_MODE="644"
    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik" sudo sh -
    cat >/var/lib/rancher/k3s/server/manifests/ingress-nginx.yaml <<EOF
    apiVersion: v1
    kind: Namespace
    metadata:
      name: ingress-nginx
    ---
    apiVersion: helm.cattle.io/v1
    kind: HelmChart
    metadata:
      name: ingress-nginx
      namespace: kube-system
    spec:
      chart: ingress-nginx
      repo: https://kubernetes.github.io/ingress-nginx
      targetNamespace: ingress-nginx
      version: v4.11.2
      set:
      valuesContent: |-
        fullnameOverride: ingress-nginx
        controller:
          kind: DaemonSet
          hostNetwork: true
          hostPort:
            enabled: true
          service:
            enabled: false
          publishService:
            enabled: false
          metrics:
            enabled: true
            serviceMonitor:
              enabled: false
          config:
            use-forwarded-headers: "true"
    EOF
```

after this you can start your vm:

```bash
#prepare no_proxy for the testdomains
export no_proxy=$no_proxy,192.168.5.15,.test

#start the vm
limactl start k3s.yaml

#configure kubectl
export KUBECONFIG="/Users/YOURUSER/.lima/docker/copied-from-guest/kubeconfig.yaml"
```

## 2. Network Setup

This guide provides instructions to configure the network setup required for running the Umbrella Chart in a Kubernetes cluster.

### Ingress Configuration

The ingress controller is automatically configured during the cluster setup with the provided K3s template. No further action is required to enable ingress.

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

Proper DNS resolution is required to map local domain names to the cluster IP address.

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

##### macOS using K3s

1. Add the values from above to your `/etc/hosts` file of your **Mac**, use `127.0.0.1` to replace the placeholder `<MINIKUBE_IP>`

2. Add the values from above to your `/etc/hosts` file of your **lima vm**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

   ```bash
   #to login to your limavm
   limactl shell k3s
   ```

3. Add the values from aboveto your coredns configuration of your **k3s-cluster**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

   ```bash
   kubectl edit cm coredns -n kube-system
   ```

   ```yaml
   apiVersion: v1
   data:
   Corefile: |
      .:53 {
         log
         errors
         health
         ready
         kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
         }
         hosts /etc/coredns/NodeHosts {
            #ADD THE HOSTS HERE
            ttl 60
            reload 15s
            fallthrough
         }
   ```

   > **Note**
   > If you do this step, after you already deployed the helm charts, make sure to  restart your java backend pods (controlplane and dataplane) to refresh their dns resolution.
   > To make this change permanent in your vm, make sure to update `/var/lib/rancher/k3s/server/manifests/coredns.yaml` in the install script of your vm template

3. Test DNS resolution by pinging one of the configured hostnames.

### Verify Network Setup

Once the DNS resolution or hosts file is configured:

1. Ensure ingress is working by accessing a service endpoint, such as <http://portal.tx.test>

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

### Troubleshooting

For common issues and solutions, please refer to the [Troubleshooting Guide](../common/troubleshooting/README.md).

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
