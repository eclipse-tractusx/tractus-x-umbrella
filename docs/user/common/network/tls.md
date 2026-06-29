# Self-Signed TLS Setup (optional)

Some umbrella components can be configured with TLS enabled. You can either:

- Use the preconfigured TLS example values file [`values-tls.yaml`](../../../../charts/umbrella/values-tls.yaml); or
- Manually enable TLS via the "uncomment the following line for tls" comments in [`values.yaml`](../../../../charts/umbrella/values.yaml).

If you'd like to make use of that, perform this step beforehand.

## Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace umbrella \
  --create-namespace \
  --version v1.18.2 \
  --set installCRDs=true
```

## Configure self-signed certificates

Create a `ClusterIssuer` and a self-signed certificate for your environment.

1. Apply the bundled configuration:

   ```bash
   kubectl apply -f ./charts/umbrella/cluster-issuer.yaml
   ```

   Alternatively, create the issuer manually:

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

   > **Note**: The `tx.test` domain is for local development only. It is a reserved
   > TLD that cannot be used with public ACME providers like Let's Encrypt.

2. Verify the `ClusterIssuer` is ready:

   ```bash
   kubectl get clusterissuer
   ```

See [cert-manager self-signed](https://cert-manager.io/docs/configuration/selfsigned) for reference.

## Apply TLS configuration

**Option 1 — Use the provided ACME values file:**

> [!WARNING]
> ACME requires publicly resolvable domains. Do not use `.test` domains with ACME.
> For local development, prefer the self-signed option below.

```bash
helm upgrade --install umbrella charts/umbrella \
  --namespace umbrella \
  -f charts/umbrella/values-tls.yaml
```

This creates an Issuer named `umbrella-ca-issuer` and annotates ingresses with
`cert-manager.io/issuer: "umbrella-ca-issuer"`.

**Option 2 — Manually annotate ingresses with the self-signed issuer:**

```yaml
portal:
  frontend:
    ingress:
      annotations:
        cert-manager.io/cluster-issuer: "my-ca-issuer"
      tls:
        - secretName: "portal.tx.test-tls"
          hosts:
            - "portal.tx.test"
            - "centralidp.tx.test"
```

Deploy the updated configuration:

```bash
helm upgrade --install umbrella charts/umbrella --namespace umbrella
```

## Testing TLS

1. Access a secured endpoint, e.g. <https://portal.tx.test>.
2. Accept the risk for the self-signed certificate in your browser, or import the
   root certificate into your trusted store.

For more details, refer to the [cert-manager documentation](https://cert-manager.io/docs/configuration/selfsigned).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
