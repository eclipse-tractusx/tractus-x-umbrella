# Self-Signed TLS Setup (optional)

Some of the components are prepared to be configured with TLS enabled. You can either:

- Use the preconfigured TLS example values file [values-tls.yaml](/charts/umbrella/values-tls.yaml); or
- Manually enable TLS via the "uncomment the following line for tls" comments in [values.yaml](/charts/umbrella/values.yaml).

If you'd like to make use of that, make sure to to execute this step beforehand.

## Install cert-manager

To manage self-signed certificates, install `cert-manager` using Helm:

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace umbrella \
  --create-namespace \
  --version v1.18.2 \
  --set installCRDs=true
```

## Configure Self-Signed Certificates

Create a `ClusterIssuer` and a self-signed certificate for your environment.

1. Apply the configuration file for the `ClusterIssuer` and the root certificate:

   If you have the repository checked out, use:

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
     namespace umbrella
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


> **Note**
> The domain "tx.test" used in this example is for local development only. This is a reserved TLD (.test) that can't be used with public ACME providers like Let's Encrypt, which don't issue certificates for `.test` domains. For a production environment, you would need to use a publicly resolvable domain name that you own.

2. Verify the `ClusterIssuer` is ready:

```bash
kubectl get clusterissuer
```

See [cert-manager self-signed](https://cert-manager.io/docs/configuration/selfsigned) for reference.

## Apply TLS Configuration

Choose one of the following approaches.

1) Use the provided TLS example values (ACME via cert-manager)

> [!WARNING]
> ACME requires publicly resolvable domains and reachable HTTP-01 validation endpoints. Do not use `.test` domains with ACME. For local development, prefer the self-signed option below.

- The repository contains an example values file that enables an ACME Issuer and configures TLS for all relevant ingresses: `charts/umbrella/values-tls.yaml`.
- This will create an Issuer named `umbrella-ca-issuer` (via `templates/ca-issuer.yaml`) and annotate ingresses with `cert-manager.io/issuer: "umbrella-ca-issuer"`.

Install or upgrade with the file:

```shell script
helm upgrade --install umbrella charts/umbrella \
  --namespace umbrella \
  -f charts/umbrella/values-tls.yaml
```


2) Manually enable TLS with the self-signed ClusterIssuer

- After you created the self-signed ClusterIssuer (`my-ca-issuer`), annotate your ingresses to use it and provide a TLS secret name. For example, in `values.yaml` under the Portal Frontend ingress:

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
helm upgrade --install umbrella . --namespace umbrella
```

## Testing TLS

1. Access one of the secured endpoints, for example:

```
https://portal.tx.test
```

2. Accept the risk for the self-signed certificate in your browser or import the root certificate into your trusted store.

For more details, refer to the [cert-manager documentation](https://cert-manager.io/docs/configuration/selfsigned).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
