- [Umbrella Chart](#umbrella-chart)
  - [Usage](#usage)
    - [Cluster setup](#cluster-setup)
    - [Network setup](#network-setup)
    - [Install](#install)
      - [Released chart](#use-released-chart)
      - [Repository](#use-local-repository)
    - [E2E Adopter Journeys](#e2e-adopter-journeys)
      - [Data exchange](#data-exchange)
      - [Get to know the Portal](#get-to-know-the-portal)
    - [Uninstall](#uninstall)
    - [Ingresses](#ingresses)
    - [Database Access](#database-access)
    - [Keycloak Admin Console](#keycloak-admin-console)
    - [Seeding](#seeding)
    - [Self-signed TLS setup (Optional)](#self-signed-tls-setup-optional)
  - [Precondition for Semantic Hub](#precondition-for-semantic-hub)
  - [How to contribute](#how-to-contribute)

# Umbrella Chart

This umbrella chart provides a basis for running end-to-end tests or creating a sandbox environment of the [Catena-X](https://catena-x.net/en/) automotive dataspace network consisting of [Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) OSS components.

The Chart aims for a completely automated setup of a fully functional network, that does not require manual setup steps.

## Usage

Running this helm chart **requires** a kubernetes cluster (`>1.24.x`), it's recommended to run it on [**Minikube**](https://minikube.sigs.k8s.io/docs/start/).
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following instructions to install the chart as `umbrella` release.

> **Note**
>
> In its current state of development, this chart as well as the following installation guide have been tested on Linux and Mac.
>
> **Linux** is the **preferred platform** to install this chart on, as the network setup with Minikube is very straightforward on Linux.
>
> We are working on testing the chart's reliability on Windows as well and updating the installation guide accordingly.

### Cluster setup

> Recommendations for resources
> | CPU(cores) | Memory(GB) |
> | :--------: | :--------: |
> |     4      |      6     |

> Use the dashboard provided by Minikube or a tool like OpenLens to get an overview about the deployed components:
>
> ```bash
> minikube dashboard
> ```

#### Linux & Mac

```bash
minikube start --cpus=4 --memory 6gb
```

#### Windows

For DNS resolution to work you need to either use `--driver=hyperv` option which requires administrator privileges:

```bash
minikube start --cpus=4 --memory 6gb --driver=hyperv
```

or use the native Kubernetes Cluster in *Docker Desktop* as well with a manual ingress setup:

```bash
# 1. Enable Kubernetes unter Settings > Kubernetes > Enable Kubernetes
# 2. Install an NGINX Ingress Controller
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
# 3. Skip the minikube addons and assume 127.0.0.1 for Cluster IP 
```

> :warning: The rest of the tutorial assumes a minikube cluster, however.

### Network setup

In order to enable the local access via **ingress**, use the according addon for Minikube:

```bash
minikube addons enable ingress
```

Make sure that the **DNS** resolution for the hosts is in place:

```bash
minikube addons enable ingress-dns
```

And execute installation step [3 Add the `minikube ip` as a DNS server](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns) for your OS:

To find out the IP address of your Minikube execute:

```bash
minikube ip
```

In the following steps, replace `192.168.49.2` with your `minikube ip` if it differs.

#### Linux & Mac
Create a file in /etc/resolver/minikube-test with the following contents.

```
domain tx.test
nameserver 192.168.49.2
search_order 1
timeout 5
```

If you still face DNS issues, add the hosts to your /etc/hosts file:

```
192.168.49.2    centralidp.tx.test
192.168.49.2    sharedidp.tx.test
192.168.49.2    portal.tx.test
192.168.49.2    portal-backend.tx.test
192.168.49.2    managed-identity-wallets.tx.test
192.168.49.2    semantics.tx.test
192.168.49.2    sdfactory.tx.test
192.168.49.2    ssi.tx.test
192.168.49.2    dataconsumer-1-dataplane.tx.test
192.168.49.2    dataconsumer-1-controlplane.tx.test
192.168.49.2    dataprovider-dataplane.tx.test
192.168.49.2    dataconsumer-2-dataplane.tx.test
192.168.49.2    dataconsumer-2-controlplane.tx.test
```

**Additional network setup for Mac**

Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

We also recommend to execute the usage example after install to check proper setup.

#### Windows

For Windows edit the hosts file under `C:\Windows\System32\drivers\etc\hosts`:

```
192.168.49.2    centralidp.tx.test
192.168.49.2    sharedidp.tx.test
192.168.49.2    portal.tx.test
192.168.49.2    portal-backend.tx.test
192.168.49.2    managed-identity-wallets.tx.test
192.168.49.2    semantics.tx.test
192.168.49.2    sdfactory.tx.test
192.168.49.2    ssi.tx.test
192.168.49.2    dataconsumer-1-dataplane.tx.test
192.168.49.2    dataconsumer-1-controlplane.tx.test
192.168.49.2    dataprovider-dataplane.tx.test
192.168.49.2    dataconsumer-2-dataplane.tx.test
192.168.49.2    dataconsumer-2-controlplane.tx.test
```

### Install

Select a subset of components which are designed to integrate with each other for a certain functional use case and enable those at install.

The currently available components are following:

- [portal](https://github.com/eclipse-tractusx/portal/tree/portal-2.0.0)
- [centralidp](https://github.com/eclipse-tractusx/portal-iam/tree/v3.0.0)
- [sharedidp](https://github.com/eclipse-tractusx/portal-iam/tree/v3.0.0)
- [bpndiscovery](https://github.com/eclipse-tractusx/sldt-bpn-discovery/tree/bpndiscovery-0.2.2)
- [discoveryfinder](https://github.com/eclipse-tractusx/sldt-discovery-finder/tree/discoveryfinder-0.2.2)
- [sdfactory](https://github.com/eclipse-tractusx/sd-factory/tree/sdfactory-2.1.12)
- [managed-identity-wallet](https://github.com/eclipse-tractusx/managed-identity-wallet/tree/v0.4.0)
- [semantic-hub](https://github.com/eclipse-tractusx/sldt-semantic-hub/tree/semantic-hub-0.2.2)
- [ssi credential issuer](https://github.com/eclipse-tractusx/ssi-credential-issuer/tree/v1.0.0)
- [dataconsumerOne](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.5.3), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0))
- [tx-data-provider](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.5.3), [digital-twin-registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/digital-twin-registry-0.4.5), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0), [simple-data-backend](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/simple-data-backend))
- [dataconsumerTwo](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider) ([tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.5.3), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0))

> :warning: **Note**
>
> - Due to resource restrictions, it's **not recommended** to install the helm chart with all components enabled.
>
> - It is to be expected that some pods - which run as post-install hooks, like for instance the **portal-migrations job - will run into errors until another component**, like for instance a database, is ready to take connections.
> Those jobs will recreate pods until one run is successful.
>
> - **Persistance is disabled by default** but can be configured in a custom values file.

#### Use released chart

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
```

**:grey_question: Command explanation**

> `helm install` is used to install a chart in Kubernetes using Helm.
> > `--set COMPONENT_1.enabled=true,COMPONENT_2.enabled=true` Enables the components by setting their respective enabled values to true.
> 
> > `umbrella` is the release name for the chart.
> 
> > `tractusx-dev/umbrella` specifies the chart to install, with *tractusx-dev* being the repository name and *umbrella* being the chart
name.
> 
> > `--namespace umbrella` specifies the namespace in which to install the chart.
>
> > `--create-namespace` create a namespace with the name `umbrella`.

##### Option 1

Install with your chosen components enabled:

```bash
helm install \
  --set COMPONENT_1.enabled=true,COMPONENT_2.enabled=true,COMPONENT_3.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

##### Option 2

Choose to install one of the predefined subsets (currently in focus of the **E2E Adopter Journey**):

**Data Exchange Subset**

```bash
helm install \
  --set centralidp.enabled=true,managed-identity-wallet.enabled=true,dataconsumerOne.enabled=true,tx-data-provider.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

*Optional*

Enable `dataconsumerTwo` at upgrade:

```bash
helm install \
  --set centralidp.enabled=true,managed-identity-wallet.enabled=true,dataconsumerOne.enabled=true,tx-data-provider.enabled=true,dataconsumerTwo.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella
```

**Portal Subset**

```bash
helm install \
  --set portal.enabled=true,centralidp.enabled=true,sharedidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella \
  --create-namespace
```

To set your own configuration and secret values, install the helm chart with your own values file:

```bash
helm install -f your-values.yaml umbrella tractusx-dev/umbrella --namespace umbrella --create-namespace
```

#### Use local repository

Make sure to clone the [tractus-x-umbrella](https://github.com/eclipse-tractusx/tractus-x-umbrella) repository beforehand.

Then navigate to the chart directory:

```bash
cd charts/umbrella/
```

Download the chart dependencies:

```bash
helm dependency update
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

##### Option 1

Install your chosen components by having them enabled in a `your-values.yaml` file:

```bash
helm install -f your-values.yaml umbrella . --namespace umbrella --create-namespace
```

> In general, all your specific configuration and secret values should be set by installing with an own values file.

##### Option 2

Choose to install one of the predefined subsets (currently in focus of the **E2E Adopter Journey**):

**Data Exchange Subset**

```bash
helm install -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella --create-namespace
```

*Optional*

Enable `dataconsumerTwo` by setting it true in `values-adopter-data-exchange.yaml` and then executing an upgrade:

```bash
dataconsumerTwo:
  enabled: true
```

```bash
helm upgrade -f values-adopter-data-exchange.yaml umbrella . --namespace umbrella
```

**Portal Subset**

```bash
helm install -f values-adopter-portal.yaml umbrella . --namespace umbrella --create-namespace
```

### E2E Adopter Journeys

#### Data exchange

Involved components:

EDC, MIW, DTR, Vault (data provider and consumer in tx-data-provider), CentralIdP.

TBD.

#### Get to know the Portal

Perform first login and send out an invitation to a company to join the network (SMTP account required to be configured in custom values.yaml file).

Proceed with the login to the <http://portal.tx.test> to verify that everything is setup as expected.

Credentials to log into the initial example realm (CX-Operator):

```
cx-operator@tx.test
```

```
tractusx-umbr3lla!
```

```mermaid
%%{
  init: {
    'flowchart': { 'diagramPadding': '10', 'wrappingWidth': '', 'nodeSpacing': '', 'rankSpacing':'', 'titleTopMargin':'10', 'curve':'basis'},
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#b3cb2d',
      'primaryBorderColor': '#ffa600',
      'lineColor': '#ffa600',
      'tertiaryColor': '#fff'
    }
  }
}%%
        graph TD
          classDef stroke stroke-width:2px
          classDef addext fill:#4cb5f5,stroke:#b7b8b6,stroke-width:2px
          iam1(IAM: centralidp Keycloak):::stroke
          iam2(IAM: sharedidp Keycloak):::stroke
          portal(Portal):::stroke
          subgraph Login Flow
              iam1 --- portal & iam2
            end
          linkStyle 0,1 stroke:lightblue
```

The relevant hosts are the following:

- <http://centralidp.tx.test/auth/>
- <http://sharedidp.tx.test/auth/>
- <http://portal-backend.tx.test>
- <http://portal.tx.test>

In case that you have TLS enabled (see [Self-signed TLS setup (Optional)](#self-signed-tls-setup-optional)), make sure to accept the risk of the self-signed certificates for all the hosts before performing the first login:

- <https://centralidp.tx.test/auth/>
- <https://sharedidp.tx.test/auth/>
- <https://portal-backend.tx.test>
- <https://portal.tx.test>

### Uninstall

To teardown your setup, run:

```shell
helm delete umbrella --namespace umbrella
```

> :warning:
>
> If persistance for one or more components is enabled, the persistent volume claims (PVCs) and connected persistent volumes (PVs) need to be removed manually even if you deleted the release from the cluster.
>

### Ingresses

Currently enabled ingresses:

- http://centralidp.tx.test/auth/
- http://sharedidp.tx.test/auth/
- http://portal-backend.tx.test
  - http://portal-backend.tx.test/api/administration/swagger/index.html
  - http://portal-backend.tx.test/api/registration/swagger/index.html
  - http://portal-backend.tx.test/api/apps/swagger/index.html
  - http://portal-backend.tx.test/api/services/swagger/index.html
  - http://portal-backend.tx.test/api/notification/swagger/index.html
- http://portal.tx.test
- http://managed-identity-wallets.tx.test/ui/swagger-ui/index.html
- http://semantics.tx.test/discoveryfinder/swagger-ui/index.html
- http://ssi.tx.test/
- http://dataconsumer-1-controlplane.tx.test
- http://dataconsumer-1-dataplane.tx.test
- http://dataprovider-dataplane.tx.test
- http://dataconsumer-2-controlplane.tx.test
- http://dataconsumer-2-dataplane.tx.test
- http://pgadmin4.tx.test

### Database Access

This chart also contains a pgadmin4 instance for easy access to the deployed Postgres databases which are only available from within the Kubernetes cluster.

pgadmin4 is by default enabled with in the predefined subsets for data exchange and portal.

Address: [pgadmin4.tx.test](http://pgadmin4.tx.test)

Credentials to login into pgadmin4:

```
pgadmin4@txtest.org
```

```
tractusxpgdamin4
```

**The database server connections need to be added manually to pgadmin4.**

Default username for all connections:

```
postgres
```

Default user for all connections:

```
5432
```

In the following some of the available connections:

- portal

Host:

```
portal-backend-postgresql
```

Password:

```
dbpasswordportal
```

- centralidp

Host:

```
umbrella-centralidp-postgresql
```

Password:

```
dbpasswordcentralidp
```

- sharedidp

Host:

```
umbrella-sharedidp-postgresql
```

Password:

```
dbpasswordsharedidp
```

- miw

Host:

```
umbrella-miw-postgres
```

Password:

```
dbpasswordmiw
```

- dataprovider

Host:

```
umbrella-dataprovider-db
```

Password:

```
dbpasswordtxdataprovider
```

- dataconsumer-1

Host:

```
umbrella-dataconsumer-1-db
```

Password:

```
dbpassworddataconsumerone
```

- dataconsumer-2

Host:

```
umbrella-dataconsumer-2-db
```

Password:

```
dbpassworddataconsumertwo
```
### Keycloak Admin Console

Access to admin consoles:

- http://centralidp.tx.test/auth/
- http://sharedidp.tx.test/auth/

Default username for centralidp and sharedidp:

```
admin
```

Password centralidp:

```
adminconsolepwcentralidp
```

Password sharedidp:

```
adminconsolepwsharedidp
```


### Seeding

See [Overall Seeding](../../concept/seeds-overall-data.md).

### Self-signed TLS setup (Optional)

Some of the components are prepared to be configured with TLS enabled (see "uncomment the following line for tls" comments in [values.yaml](./values.yaml)).

If you'd like to make use of that, make sure to to execute this step beforehand.

Install cert-manager chart in the same namespace where the umbrella chart will be located.

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace umbrella \
  --create-namespace \
  --version v1.14.4 \
  --set installCRDs=true
```

Configure the self-signed certificate and issuer to be used by the ingress resources.

If you have the repository checked out you can run:

```bash
kubectl apply -f ./charts/umbrella/cluster-issuer.yaml
```

or otherwise you can run:

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-selfsigned-ca
  namespace: umbrella
spec:
  isCA: true
  commonName: tx.test
  secretName: root-secret
  privateKey:
    algorithm: RSA
    size: 2048
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
    group: cert-manager.io
  subject:
    organizations:
      - CX
    countries:
      - DE
    provinces:
      - Some-State
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: my-ca-issuer
spec:
  ca:
    secretName: root-secret
EOF
```

See [cert-manager self-signed](https://cert-manager.io/docs/configuration/selfsigned) for reference.

## Precondition for Semantic Hub

In case of enabling `semantic-hub` the fuseki docker image must be built.
Build fuseki docker image by following the below steps:
- Download [jena-fuseki-docker-4.7.0.zip](https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-docker/4.7.0/jena-fuseki-docker-4.7.0.zip)
- Unzip the jena-fuseki-docker-4.7.0.zip.
- Build the docker image by running the command - `docker build --build-arg JENA_VERSION=4.7.0 -t jena-fuseki-docker:4.7.0 --platform linux/amd64 .`

## How to contribute

Before contributing, make sure, you read and understand our [contributing guidelines](/CONTRIBUTING.md).
We appreciate every contribution, be it bug reports, feature requests, test automation or enhancements to the Chart(s),
but please keep the following in mind:

- Avoid company specific setup
- Avoid any tooling/infra components, that requires a subscription in any form
- Be vendor and cloud agnostic
