# Windows Setup Handover — tractus-x-umbrella

Getting the umbrella chart (data-exchange subset) running on **Windows + minikube (docker driver)**.
The repo is untested on Windows; these are the fixes that were needed beyond the docs.

## Environment

- Windows 11, Docker Desktop, minikube `--driver=docker`
- Tools installed: minikube, kubectl, helm (via winget / .exe; PATH set at User scope)
- Cluster: `minikube start --cpus=4 --memory=6gb --driver=docker`

## Problems hit & fixes

### 1. Proxy breaks kubectl/helm — `invalid character '<'`
Corporate proxy returned an HTML error page for cluster API calls.
**Fix:** set `NO_PROXY` (persist at User scope), then use a fresh shell:
```powershell
[Environment]::SetEnvironmentVariable('NO_PROXY',
  "localhost,127.0.0.1,10.96.0.0/12,192.168.49.0/24,192.168.59.0/24,.svc,.cluster.local", 'User')
```

### 2. API server port changes on restart
docker driver randomizes the kube-apiserver port each `minikube start`; kubectl then hits a stale port and returns `<`.
**Fix:** after every start/restart:
```powershell
minikube update-context
```

### 3. helm upgrade → vault webhook conflict
`helm upgrade` fails with a `MutatingWebhookConfiguration` `caBundle` conflict (vault-k8s owns that field via server-side apply).
**Fix:** always uninstall + install for redeploys:
```powershell
helm uninstall umbrella -n umbrella
kubectl delete mutatingwebhookconfiguration `
  umbrella-edc-dataconsumer-1-vault-agent-injector-cfg `
  umbrella-edc-dataprovider-vault-agent-injector-cfg --ignore-not-found
helm install -f values-adopter-data-exchange.yaml umbrella . `
  --namespace umbrella --create-namespace --timeout 20m
```

### 4. testdata post-install job fails — `ssi-dim-wallet-stub.tx.test: Name does not resolve` (THE main blocker)
EDC does in-cluster DID resolution against `*.tx.test` ingress hostnames. CoreDNS has no `tx.test`
zone on Windows/docker (the `ingress-dns` addon does not wire it up). The documented resolv.conf
`search`-line fix does **not** apply — the docker node's `/etc/resolv.conf` has no `search` line.

**Fix:** patch CoreDNS to resolve `*.tx.test` to the ingress-nginx-controller ClusterIP.
Get the ClusterIP: `kubectl get svc -n ingress-nginx ingress-nginx-controller` (was `10.108.83.156`).
Add this zone to the `coredns` ConfigMap (kube-system), above the `.:53` block:
```
tx.test:53 {
    errors
    cache 30
    template IN A {
        answer "{{ .Name }} 60 IN A 10.108.83.156"
    }
    template IN AAAA {
    }
}
```
Then:
```powershell
kubectl apply -f coredns-cm.yaml
kubectl rollout restart deployment coredns -n kube-system
# verify:
kubectl run dnstest --image=busybox:1.36 --restart=Never --rm -i -- nslookup ssi-dim-wallet-stub.tx.test
```
> NOT persistent — reapply after `minikube stop/start`. If the ingress ClusterIP changes, update the answer IP.

### 5. Browser access to services
`C:\Windows\System32\drivers\etc\hosts` (admin) maps `*.tx.test` → `minikube ip` (192.168.49.2)
for the **browser only** — this does NOT affect in-cluster pod resolution (that's #4).
With the docker driver, verify the minikube IP is reachable from the host (`ping 192.168.49.2`);
if not, use `minikube tunnel` and point hosts entries at `127.0.0.1`.

## Order of operations (clean run)

1. `minikube start --cpus=4 --memory=6gb --driver=docker`
2. `minikube addons enable ingress` + `ingress-dns`
3. `minikube update-context`; ensure `NO_PROXY` set
4. `helm dependency update` (or `bash hack/helm-dependencies.bash`)
5. **Apply CoreDNS patch (#4)** — before install, or the testdata job fails
6. `helm install ... --timeout 20m` from `charts/umbrella`
7. Add Windows hosts entries (#5) for browser access

## Open items / not-permanent

- CoreDNS patch + hosts file must be re-applied if minikube is recreated.
- Consider baking #4 into the chart / an addon for a proper Windows contribution (repo requests Windows PRs).
