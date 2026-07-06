# macOS Deployment Guide (with Rancher Desktop)

This guide combines the steps for Cluster Setup, Network Setup, and Installation for macOS users using [Rancher Desktop](https://rancherdesktop.io/) with its built-in Kubernetes (K3s).

> [!NOTE]
> Rancher Desktop ships Kubernetes as [K3s](https://k3s.io/) running inside a Lima VM. By default K3s bundles the **Traefik** ingress controller, but the Umbrella charts are written for the **NGINX** ingress controller. This guide therefore disables Traefik and installs `ingress-nginx` instead.

## 1. Cluster Setup

This guide provides instructions to set up a Kubernetes cluster required for running the Umbrella Chart.

### System Requirements

| CPU (Cores) | Memory (GB) |
| :----------:| :----------:|
|      4      |      6      |

The above specifications are the minimum requirements for a local development setup. Adjust resources based on your workload for larger or production environments.

### Install Rancher Desktop

Install Rancher Desktop either from the [official website](https://rancherdesktop.io/) or via Homebrew:

```bash
brew install --cask rancher-desktop
```

### Configure and Enable Kubernetes

1. Open **Rancher Desktop** and go to **Preferences**.

2. Under **Virtual Machine → Hardware**, assign at least the resources from the table above (e.g. **4 CPUs** and **6 GB memory**). More is recommended if you plan to run larger subsets.

3. Under **Kubernetes**:
   - Make sure **Enable Kubernetes** is checked.
   - **Uncheck** **Enable Traefik**. The Umbrella charts require the NGINX ingress controller, which you will install in the next section.
   - Select a recent, supported Kubernetes version.

4. Apply the changes and wait until Rancher Desktop reports that Kubernetes is running.

5. Rancher Desktop automatically sets your `kubectl` context to `rancher-desktop`. Verify the cluster is reachable:

   ```bash
   kubectl config use-context rancher-desktop
   kubectl get nodes
   ```

## 2. Network Setup

This guide provides instructions to configure the network setup required for running the Umbrella Chart in a Kubernetes cluster.

### Install the NGINX Ingress Controller

Since Traefik was disabled during cluster setup, install `ingress-nginx` with Helm:

```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.watchIngressWithoutClass=true \
  --set controller.ingressClassResource.default=true
```

> [!IMPORTANT]
> `controller.watchIngressWithoutClass=true` is **required**. Several of the
> Umbrella ingresses (the `*.local` / `*.intranet` hosts and `issuerservice.local`)
> are created **without** an explicit `ingressClassName`. By default `ingress-nginx`
> **ignores** class-less ingresses (you would see `ignoring ingress ... : ingress
> does not contain a valid IngressClass` in the controller log and get an
> **nginx 404** on those hosts), so the controller must be told to watch them.
> `controller.ingressClassResource.default=true` additionally marks NGINX as the
> default class so any *newly created* class-less ingress is adopted too — but note
> the default-class annotation only mutates ingresses at creation time, so
> `watchIngressWithoutClass` is what actually serves the already-installed ones.
> On Minikube the ingress addon already watches class-less ingresses, which is why
> the Docker Desktop guide does not need these flags.
>
> If you installed `ingress-nginx` earlier without this flag, apply it and roll the
> controller:
>
> ```bash
> helm upgrade ingress-nginx ingress-nginx \
>   --repo https://kubernetes.github.io/ingress-nginx \
>   --namespace ingress-nginx --reuse-values \
>   --set controller.watchIngressWithoutClass=true
> kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller
> ```

Rancher Desktop forwards `LoadBalancer` services to `localhost` (`127.0.0.1`) on your Mac. Wait until the controller is ready:

```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s
```

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

Proper DNS resolution is required to map local domain names to the cluster. With Rancher Desktop the ingress controller is reachable on `localhost`, so the hostnames resolve to `127.0.0.1` (the `.local` hosts additionally need an IPv6 `::1` entry — see the note below).

#### Hosts File Configuration

The following values need to be added in each case:

   ```text
   127.0.0.1    centralidp.tx.test
   127.0.0.1    sharedidp.tx.test
   127.0.0.1    portal.tx.test
   127.0.0.1    portal-backend.tx.test
   127.0.0.1    semantics.tx.test
   127.0.0.1    sdfactory.tx.test
   127.0.0.1    ssi-credential-issuer.tx.test
   127.0.0.1    dataconsumer-1-dataplane.tx.test
   127.0.0.1    dataconsumer-1-controlplane.tx.test
   127.0.0.1    dataprovider-dataplane.tx.test
   127.0.0.1    dataprovider-controlplane.tx.test
   127.0.0.1    dataprovider-submodelserver.tx.test
   127.0.0.1    dataconsumer-2-dataplane.tx.test
   127.0.0.1    dataconsumer-2-controlplane.tx.test
   127.0.0.1    bdrs-server.tx.test
   127.0.0.1    business-partners.tx.test
   127.0.0.1    pgadmin4.tx.test
   127.0.0.1    ssi-dim-wallet-stub.tx.test
   127.0.0.1    smtp.tx.test
   ```

   **For the Decentralized IdentityHub profile (recommended), also add:**

   ```text
   127.0.0.1    provider.local
   127.0.0.1    provider.intranet
   127.0.0.1    consumer.local
   127.0.0.1    consumer.intranet
   127.0.0.1    issuerservice.local
   # IPv6 (see the .local note below) — required to avoid a 5s delay per request
   ::1          provider.local
   ::1          consumer.local
   ::1          issuerservice.local
   ```

> [!IMPORTANT]
> **macOS `.local` gotcha.** macOS reserves the `.local` suffix for Multicast
> DNS (Bonjour, RFC 6762). With only an IPv4 (`127.0.0.1`) entry, the IPv4
> lookup resolves from `/etc/hosts` instantly, but the IPv6 (`AAAA`) lookup has
> no matching entry and is sent to mDNS, which **waits ~5 seconds** before
> failing back. Because browsers and `curl` do a dual-stack lookup, every
> request to a `.local` host stalls for ~5s. Adding the `::1` entries above
> makes the IPv6 lookup resolve from `/etc/hosts` too and removes the delay.
> The `.test` and `.intranet` hosts are not affected (those suffixes are not
> mDNS-reserved).

##### macOS using Rancher Desktop

1. Open the hosts file you find here: `/etc/hosts` and insert the values from above.
   The `.tx.test` / `.intranet` hosts map to `127.0.0.1`; the `.local` hosts get
   both a `127.0.0.1` and a `::1` entry (see the note above).

2. Test DNS resolution and ingress by requesting one of the configured hostnames:

   ```bash
   curl -sm5 -o /dev/null -w "%{http_code}\n" http://portal.tx.test/
   # For a .local host, an HTTP response returning quickly (not after ~5s)
   # confirms the ::1 entries are working:
   curl -sm5 -o /dev/null -w "namelookup=%{time_namelookup}s %{http_code}\n" http://provider.local/
   ```

### Verify Network Setup

Once the hosts file is configured:

1. Ensure ingress is working by accessing a service endpoint, such as <http://portal.tx.test>

### Troubleshooting

For common issues and solutions, please refer to the [Troubleshooting Guide](../common/troubleshooting/README.md).

Rancher-Desktop-specific notes:

- **`*.local` / `issuerservice.local` hosts return an nginx 404** &mdash; the
  controller is ignoring the class-less ingresses. Ensure it was installed with
  `controller.watchIngressWithoutClass=true` (see the note above) and that these
  hosts are in `/etc/hosts` pointing to `127.0.0.1`. Confirm with
  `kubectl -n ingress-nginx logs deploy/ingress-nginx-controller | grep -i "ignoring ingress"`.
- **Pods restart a few times before becoming `Ready` (CrashLoopBackOff)** &mdash;
  slow-starting Java services (e.g. `issuerservice`, `digital-twin-registry`) can
  trip their liveness probe on the first boot while running schema migrations or
  under CPU throttling. They usually self-recover after 1&ndash;5 restarts. If a pod
  never stabilises, give the VM more CPU/memory in **Rancher Desktop → Preferences →
  Virtual Machine → Hardware** and redeploy.

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
helm dependency update charts/decentralized-identity-connector
helm dependency update charts/umbrella
```

> [!IMPORTANT]
> `charts/decentralized-identity-connector` is a dependency-only aggregator chart
> (it has no templates of its own — the provider and consumer EDCs come entirely
> from its sub-charts). Its dependencies **must** be built **before** the umbrella
> chart, otherwise it gets packaged empty and the `edc-provider` / `edc-consumer`
> components deploy nothing even though they are enabled in
> `values-adopter-decentralized-identityhub.yaml`.

Navigate to the `charts/umbrella` directory.
```bash
cd charts/umbrella/
```

> [!NOTE]
> **Do not run anything yet.** All install commands you will use below follow the
> same pattern &mdash; the snippet here is just a reference so you understand the
> flags. Pick one of the subsets in the sections that follow
> ([Decentralized IdentityHub](#decentralized-identityhub-subset-recommended-default),
> [Data Exchange (legacy)](#data-exchange-subset-legacy-centralized-flow) or
> [Portal](#portal-subset)) and run the command listed there.

```bash
helm install -f <values-file>.yaml umbrella . --namespace umbrella --create-namespace
```

<details>
<summary><strong>❓ What does each flag mean?</strong></summary>

<br/>

- `helm install` &mdash; installs a Helm chart.
- `-f <values-file>.yaml` &mdash; values file used for configuration (e.g. `values-adopter-decentralized-identityhub.yaml` or your own `your-values.yaml`).
- `umbrella` &mdash; release name of the Helm chart.
- `.` &mdash; path to the chart directory (the current `charts/umbrella/` folder).
- `--namespace umbrella` &mdash; target Kubernetes namespace.
- `--create-namespace` &mdash; create the `umbrella` namespace if it does not exist.

</details>

### Custom Configuration

Install your chosen components by having them enabled in a `your-values.yaml` file:

```bash
helm install -f your-values.yaml umbrella . --namespace umbrella --create-namespace
```

> In general, all your specific configuration and secret values should be set by installing with an own values file.

Choose to install one of the predefined subsets (currently in focus of the **E2E Adopter Journey**):

### Decentralized IdentityHub Subset (recommended default)

Since Release 25.12 this is the recommended scenario — it deploys a provider EDC,
a consumer EDC, the IssuerService and the BDRS server using decentralized
identifiers (`did:web`) and per-participant IdentityHubs.

> Make sure your hosts file already contains the `*.local`, `*.intranet` and
> `bdrs-server.tx.test` entries listed in the DNS resolution section above.

```bash
helm install -f values-adopter-decentralized-identityhub.yaml umbrella . --namespace umbrella --create-namespace
```

See [Data Exchange with Decentralized IdentityHub](../common/guides/data-exchange-identityhub.md)
for the participant identifiers (BPNs / DIDs) and how to exercise the dataspace.

### Data Exchange Subset (legacy centralized flow)

The legacy Data Exchange subset uses CX-IAM and the centralized `ssi-dim-wallet-stub`.
Kept for backwards compatibility.

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
* SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
