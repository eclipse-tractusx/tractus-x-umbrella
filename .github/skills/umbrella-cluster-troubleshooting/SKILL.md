---
name: umbrella-cluster-troubleshooting
description: 'Diagnose a broken tractus-x-umbrella deployment. Use when: pods Pending, CrashLoopBackOff, ImagePullBackOff, OOMKilled; helm install timeout or failed post-install hook job; DNS or CoreDNS issues, *.tx.test hosts not resolving, ingress 404/502/503; DSP catalog HTTP 500; EDC, IdentityHub, IssuerService, BDRS, DTR or centralidp errors; Vault sealed, ExternalSecret not syncing, SecretStore not ready; cert-manager certificate not issued; PVC Pending; Postgres init failures.'
argument-hint: 'Symptom and namespace, e.g. edc-provider CrashLoopBackOff in umbrella'
---

# Umbrella Cluster Troubleshooting

Collect facts first, then match the symptom. Don't reinstall until you know the cause.

## 1. Collect

```bash
helm list -A
helm status umbrella -n umbrella
kubectl get pods,jobs -n umbrella -o wide
kubectl get events -n umbrella --sort-by=.lastTimestamp | tail -40
kubectl describe pod <pod> -n umbrella
kubectl logs <pod> -n umbrella --all-containers --tail=200
kubectl logs <pod> -n umbrella --previous          # after a restart
kubectl top nodes && kubectl top pods -n umbrella   # needs metrics-server
minikube addons list
```

Never print secret values. To inspect a Secret, list keys only:
```bash
kubectl get secret <name> -n umbrella -o jsonpath='{.data}' | tr ',' '\n' | cut -d: -f1
```

## 2. Match the symptom

| Symptom | Likely cause | Check / fix |
|---|---|---|
| `Pending` | Not enough CPU/memory, PVC unbound | `describe pod` events; bigger cluster; `kubectl get pvc,sc` |
| `OOMKilled` / restarts | Memory limit or node too small | `describe pod` last state; raise cluster memory or limits via values |
| `ImagePullBackOff` | Wrong tag, removed image (e.g. Bitnami changes), rate limits | `describe pod`; `docs/admin/migration-guide.md` |
| `CrashLoopBackOff` | Config error, dependency not reachable, DB not ready | `logs --previous`; check the dependency's service and DNS |
| Hosts don't resolve from the laptop | ingress-dns / host resolver not configured | OS guide DNS section |
| In-cluster DNS timeouts, DSP catalog 500, IDP crashloop | CoreDNS search-domain inheritance | `docs/user/common/troubleshooting/README.md` (custom `resolv.conf`) |
| Ingress 404 | Wrong host/path, ingress class | `kubectl get ingress -A`; ingress-nginx controller logs |
| Ingress 502/503 | Backend not ready or wrong service port | `kubectl get endpoints <svc> -n umbrella` |
| `helm install` timeout | Slow/failed post-install hook job | `kubectl get jobs`; `kubectl logs job/<job>` |
| ExternalSecret not syncing | SecretStore not ready, wrong Vault path/token | `kubectl get secretstore,externalsecret -A`; `describe externalsecret` |
| Vault errors | Vault sealed or not initialized | `kubectl exec <vault-pod> -n umbrella -- vault status` |
| TLS not working | Certificate not issued | `kubectl get certificate,certificaterequest,order,challenge -A` |
| Bruno 401/403 | Stale IssuerService `API_KEY` | `docs/common/api/bruno/README.md` |
| Windows: kubectl returns `<` | Docker driver changed apiserver port | `docs/user/windows/TROUBLESHOOTING.md` |

## 3. Fix and verify

- Prefer a values change or doc fix over manual `kubectl edit`. Manual changes are lost on the next `helm upgrade`.
- After fixing, re-run the `umbrella-deploy-verify` steps.
- If the root cause is a gap in the chart or docs, propose a PR. A new recurring failure belongs in `docs/user/common/troubleshooting/README.md`.

## 4. Clean retry (ask before running)
```bash
helm uninstall umbrella -n umbrella
kubectl delete namespace umbrella
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
