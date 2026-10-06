---
name: umbrella-deploy-verify
description: 'Deploy tractus-x-umbrella to a local Kubernetes cluster and verify it end to end. Use when: installing the umbrella on Minikube or KinD, testing a values-adopter profile (decentralized identityhub, data-exchange, portal, observability, external-secrets, tls), smoke-testing a chart change at runtime, waiting for pods and post-install jobs, checking ingress hosts, running the Bruno data exchange collections, preparing a workshop environment.'
argument-hint: 'Profile and OS, e.g. decentralized-identityhub on macOS'
---

# Umbrella Deploy & Verify

## Procedure

1. **Read the platform guide first**: `docs/user/<linux|mac|windows>/` — DNS and driver setup differ per OS.

2. **Cluster** (Minikube example, documented minimum):
   ```bash
   minikube start --cpus=4 --memory=6gb
   minikube addons enable ingress
   minikube addons enable ingress-dns
   ```
   Heavier profiles (portal, observability, several participants) need more memory. Pods stuck in `Pending` usually mean the cluster is too small.

3. **Dependencies**
   ```bash
   ./hack/helm-dependencies.bash
   ```

4. **Install** (one profile per release; don't layer legacy and decentralized profiles):
   ```bash
   helm install umbrella charts/umbrella \
     -f charts/umbrella/values-adopter-decentralized-identityhub.yaml \
     --namespace umbrella --create-namespace --timeout 20m
   ```
   For the released chart instead of local sources, see `docs/user/common/installation.md`.

5. **Wait for readiness** (completed Job pods are never `Ready`, so check them separately):
   ```bash
   kubectl get pods -n umbrella -w
   kubectl wait -n umbrella --for=condition=Ready pod \
     --field-selector=status.phase!=Succeeded --all --timeout=15m
   kubectl wait -n umbrella --for=condition=Complete job --all --timeout=15m
   ```

6. **Ingress and DNS**
   ```bash
   kubectl get ingress -n umbrella
   curl -sS -o /dev/null -w '%{http_code}\n' http://<host-from-ingress>/
   ```
   If hosts don't resolve, follow the OS guide's DNS section and `docs/user/common/troubleshooting/README.md`.

7. **Functional test (Bruno)**: follow `docs/common/api/bruno/README.md`.
   - Use the collection that matches the profile (`Data-exchange-decentralized-identityhub/` for the default, `Umbrella-bru/` for the legacy flow).
   - The IssuerService `API_KEY` changes with every deployment: read it from the IssuerService pod logs and set it in the Bruno environment.
   - Run the folders in order. A folder run retries the "Query Cached EDRs" step automatically.

8. **Report**: profile, cluster and versions (`kubectl version`, `helm version`, `minikube version`), pod and job status, ingress check, Bruno result, and any deviations from the docs. Fix the docs if a documented step no longer works.

## Cleanup (ask before running)
```bash
helm uninstall umbrella -n umbrella
kubectl delete namespace umbrella
```
PVCs may survive an uninstall; delete them for a clean retry.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
