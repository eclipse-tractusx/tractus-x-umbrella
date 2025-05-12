#!/usr/bin/env bash
set -euo pipefail

NS=kube-system
CM=coredns
TMP=$(mktemp)

# 1. pull the current Corefile out of the ConfigMap ↓
kubectl -n $NS get configmap $CM -o jsonpath='{.data.Corefile}' > "$TMP"

# 2. append the custom zone if it is not already present
# Adjust IP to your local minikube IP (192.168.49.2 is the standard Minikube IP)
grep -q '^test:53' "$TMP" || cat >>"$TMP" <<'BLOCK'

test:53 {
    errors
    cache 30
    forward . 192.168.49.2
}
BLOCK

# 3. push the modified Corefile back
kubectl -n $NS create configmap $CM \
        --from-file=Corefile="$TMP" \
        -o yaml --dry-run=client | kubectl apply -f -

# 4. restart CoreDNS pods so they load the new Corefile
kubectl -n $NS rollout restart deployment coredns
echo "✅ CoreDNS patched and restarted."