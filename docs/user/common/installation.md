# Installation Reference

> [!TIP]
> For the **recommended** end-to-end install (Decentralized IdentityHub), follow
> the [Quickstart](../quickstart.md). This page is a reference covering all
> install methods and component subsets.

The Helm chart is platform-independent. For the cluster + DNS setup specific to
your OS, see [Linux](../linux/README.md), [macOS](../mac/README.md) or
[Windows](../windows/README.md).

## Available components

The components currently shipped by the umbrella chart:

- [portal](https://github.com/eclipse-tractusx/portal/tree/portal-2.6.0)
- [centralidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.2.1)
- [sharedidp](https://github.com/eclipse-tractusx/portal-iam/tree/v4.2.1)
- [bpndiscovery](https://github.com/eclipse-tractusx/sldt-bpn-discovery/tree/bpndiscovery-0.5.1)
- [discoveryfinder](https://github.com/eclipse-tractusx/sldt-discovery-finder/tree/discoveryfinder-0.5.1)
- [sdfactory](https://github.com/eclipse-tractusx/sd-factory/tree/sdfactory-2.1.34)
- [semantic-hub](https://github.com/eclipse-tractusx/sldt-semantic-hub/tree/semantic-hub-0.5.0) — requires a [pre-built Fuseki image](setup/semantic-hub.md)
- [ssi-credential-issuer](https://github.com/eclipse-tractusx/ssi-credential-issuer/tree/v1.4.0)
- [tx-data-provider](../../../charts/tx-data-provider) — composite bundle pulling:
  - [dataspace-connector-bundle](../../../charts/dataspace-connector-bundle) — [tractusx-edc](https://github.com/eclipse-tractusx/tractusx-edc/tree/0.11.0), [vault](https://github.com/hashicorp/vault-helm/tree/v0.20.0)
  - [digital-twin-bundle](../../../charts/digital-twin-bundle) — [digital-twin-registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/digital-twin-registry-0.9.0)
  - [data-persistence-layer-bundle](../../../charts/data-persistence-layer-bundle) — [simple-data-backend](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/simple-data-backend-0.1.0)
- [bdrs](https://github.com/eclipse-tractusx/bpn-did-resolution-service/tree/0.5.7) (**in-memory** — no persistence)
- [bpdm](https://github.com/eclipse-tractusx/bpdm/tree/release/7.1.x)
- [identity-and-trust-bundle](../../../charts/identity-and-trust-bundle) — [ssi-dim-wallet-stub](https://github.com/eclipse-tractusx/ssi-dim-wallet-stub/tree/ssi-dim-wallet-stub-memory-0.1.11)

**Auxiliary components:**

- [external-secrets](https://github.com/external-secrets/external-secrets/tree/v0.18.2)
- [pgadmin4](https://artifacthub.io/packages/helm/runix/pgadmin4/1.25.0)
- [opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/opentelemetry-collector-0.90.0)
- [jaeger](https://github.com/jaegertracing/helm-charts/tree/jaeger-3.0.7)
- [prometheus](https://github.com/prometheus-community/helm-charts/tree/prometheus-27.1.08)
- [grafana](https://github.com/grafana/helm-charts/tree/grafana-8.10.1)
- [loki](https://github.com/grafana/loki/tree/helm-loki-6.27.0)

> **Notes**
>
> - Due to resource limits, installing **all components at once is not recommended** on a local cluster. Pick a profile (see below).
> - Some post-install jobs (e.g. portal migrations) may retry until their dependencies are ready.
> - **Persistence is disabled by default**; enable it explicitly in a custom values file.

## Install from the local repository (recommended for development)

Clone this repository, then resolve all Helm dependencies (handles the inter-chart `file://` links):

```bash
./hack/helm-dependencies.bash
```

Then install with the profile you need:

```bash
# Recommended (Decentralized IdentityHub)
helm install umbrella charts/umbrella \
  -f charts/umbrella/values-adopter-decentralized-identityhub.yaml \
  --namespace umbrella --create-namespace

# Legacy data exchange (CX-IAM + ssi-dim-wallet-stub)
helm install umbrella charts/umbrella \
  -f charts/umbrella/values-adopter-data-exchange.yaml \
  --namespace umbrella --create-namespace

# Portal-only
helm install umbrella charts/umbrella \
  -f charts/umbrella/values-adopter-portal.yaml \
  --namespace umbrella --create-namespace
```

### Enable additional data consumers

`dataconsumerTwo` is off by default. To enable it:

1. Edit your values file:

   ```yaml
   dataconsumerTwo:
     enabled: true
   ```

2. Upgrade:

   ```bash
   helm upgrade -f <your-values.yaml> umbrella charts/umbrella --namespace umbrella
   ```

## Install from the released chart

If you don't want to clone the repo, add the published Tractus-X charts repository:

```bash
helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
helm repo update
```

Then install with `--set` flags to enable the subsets you need:

```bash
# Data exchange subset
helm install \
  --set identity-and-trust-bundle.enabled=true,dataconsumerOne.enabled=true,tx-data-provider.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella --create-namespace

# Portal subset
helm install \
  --set portal.enabled=true,centralidp.enabled=true,sharedidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella --create-namespace

# BPDM subset
helm install \
  --set bpdm.enabled=true,centralidp.enabled=true \
  umbrella tractusx-dev/umbrella \
  --namespace umbrella --create-namespace
```

Or use your own values file:

```bash
helm install -f your-values.yaml umbrella tractusx-dev/umbrella \
  --namespace umbrella --create-namespace
```

## Uninstall

```bash
helm delete umbrella --namespace umbrella
```

If persistence was enabled, clean up the PVCs:

```bash
kubectl get pvc --namespace umbrella
kubectl delete pvc <pvc-name> --namespace umbrella
```

To remove the whole namespace:

```bash
kubectl delete namespace umbrella
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
