# Quickstart — Decentralized IdentityHub

> **Recommended path since Release 25.12.** This is the deployment the project is
> standardising on. If you only read one page in this repo, read this one.

It walks you from an empty Linux machine to a working dataspace (provider +
consumer + issuer) on Minikube, using the
[`values-adopter-decentralized-identityhub.yaml`](../../charts/umbrella/values-adopter-decentralized-identityhub.yaml)
profile.

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Kubernetes (Minikube preferred) | 1.24+ |
| Helm | 3.12+ |
| `kubectl` | matching your cluster |
| 4 CPU cores / 6 GB RAM free | – |

> **macOS / Windows users:** the cluster + DNS setup is different. Do the per-OS
> setup once ([macOS](mac/README.md) · [Windows](windows/README.md)), then come back
> to step 3 of this guide.

---

## 1. Start the cluster

```bash
minikube start --cpus=4 --memory=6gb
minikube addons enable ingress
minikube addons enable ingress-dns
```

## 2. Wire DNS

The decentralized profile uses `*.local` and `*.intranet` hostnames per
participant, plus `bdrs-server.tx.test`. Add them to `/etc/hosts` (Linux/macOS) or
the Windows hosts file:

```text
<MINIKUBE_IP>    provider.local
<MINIKUBE_IP>    provider.intranet
<MINIKUBE_IP>    consumer.local
<MINIKUBE_IP>    consumer.intranet
<MINIKUBE_IP>    issuerservice.local
<MINIKUBE_IP>    bdrs-server.tx.test
```

Get `<MINIKUBE_IP>` with `minikube ip`.

> Linux users who prefer not to edit `/etc/hosts` can configure systemd-resolved /
> NetworkManager / dnsmasq instead — see [Linux DNS alternatives](linux/README.md#dns-resolution-setup).

## 3. Update Helm dependencies

```bash
./hack/helm-dependencies.bash
```

> This is the one helper script you should always use; it walks the inter-chart
> `file://` dependencies in the correct order.

## 4. Install the chart

```bash
helm install umbrella charts/umbrella \
  -f charts/umbrella/values-adopter-decentralized-identityhub.yaml \
  --namespace umbrella --create-namespace
```

Wait for all pods to become `Ready`:

```bash
kubectl get pods -n umbrella -w
```

> Initial pulls + post-install jobs (BDRS seeding, IssuerService attestation
> seeding) take a few minutes the first time.

## 5. Verify the deployment

| Component | URL |
|-----------|-----|
| Provider EDC (DSP)        | <http://provider.local> |
| Provider EDC (management) | <http://provider.intranet> |
| Consumer EDC (DSP)        | <http://consumer.local> |
| Consumer EDC (management) | <http://consumer.intranet> |
| IssuerService             | <http://issuerservice.local> |
| BDRS server               | <http://bdrs-server.tx.test> |

Participant identifiers:

| Participant | BPN | DID |
|-------------|-----|-----|
| Provider      | `BPNL000000000001` | `did:web:provider.local:identityhub:BPNL000000000001` |
| Consumer      | `BPNL000000000002` | `did:web:consumer.local:identityhub:BPNL000000000002` |
| IssuerService | `BPNL000000000003` | `did:web:issuerservice.local:BPNL000000000003`        |

## 6. Try the data exchange

The fastest way to exercise the dataspace is the **Bruno collection** shipped
under [`docs/common/api/bruno/Data-exchange-decentralized-identityhub/`](../common/api/README.md).
It covers the full flow: bootstrap issuer → issue credentials → publish asset →
negotiate contract → transfer data.

Step-by-step references:

- [Provide data (asset / policy / contract definition)](common/guides/data-exchange/provide-data.md)
- [Consume data (catalog → negotiation → EDR → transfer)](common/guides/data-exchange/consume-data.md)
- [Credential issuance flow](common/guides/data-exchange/issuance.md)

---

## Uninstall

```bash
helm uninstall umbrella -n umbrella
kubectl delete pvc --all -n umbrella
kubectl delete namespace umbrella
```

---

## Going further

- **Different scenario?** See [other adopter profiles](../README.md#3-other-scenarios).
- **Real secrets backend?** Switch to [External Secrets + Vault](common/guides/external-secrets.md).
- **TLS / certificates?** See [`values-tls.yaml`](../../charts/umbrella/values-tls.yaml).
- **Stuck?** Check the [troubleshooting guide](common/troubleshooting/README.md).

---

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
