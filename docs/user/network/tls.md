# Self-Signed TLS Setup (optional)

Some of the components are prepared to be configured with TLS enabled (see "uncomment the following line for tls" comments in [values.yaml](/charts/umbrella/values.yaml)).

If you'd like to make use of that, make sure to to execute this step beforehand.

## Install cert-manager

To manage self-signed certificates, install `cert-manager` using Helm:

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace umbrella \
  --create-namespace \
  --version v1.14.4 \
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

2. Verify the `ClusterIssuer` is ready:

   ```bash
   kubectl get clusterissuer
   ```

See [cert-manager self-signed](https://cert-manager.io/docs/configuration/selfsigned) for reference.

## Apply TLS Configuration

Update the `values.yaml` file for your deployment to use TLS for ingress resources. Uncomment or add the necessary lines to enable TLS, for example:

```yaml
ingress:
  annotations:
    kubernetes.io/tls-acme: "true"
  tls:
    - secretName: tls-secret
      hosts:
        - portal.tx.test
        - centralidp.tx.test
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
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
