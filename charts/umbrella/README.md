# Umbrella Chart

This umbrella chart provides a basis for running end-to-end tests or creating a sandbox environment of the [Catena-X](https://catena-x.net/en/) automotive dataspace network
consisting of [Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) OSS components.

The chart aims for a completely automated setup of a fully functional network, that does not require manual setup steps.

## Installing

Running this Chart requires a kubernetes cluster `>1.24.x`. One of the options is to run a local instance of [minikube](https://minikube.sigs.k8s.io/docs/start/) setup.
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following command to install
the chart as `umbrella` release.

### (Optional) Self-signed TLS setup

Install cert-manager chart in the same namespace where the umbrella chart will be located.

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace umbrella \
  --create-namespace \
  --version v1.14.4 \
  --set installCRDs=true
```

Configure the self-signed certificate and issuer to be used by the ingress resources.

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
  commonName: cx.local
  secretName: root-secret
  privateKey:
    algorithm: RSA
    size: 2048
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
    group: cert-manager.io
  subject:
    organizations:
      - CX
    countries:
      - DE
    provinces:
      - Some-State
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

See [cert-manager self-signed](https://cert-manager.io/docs/configuration/selfsigned) for reference.

### Installing the chart

```shell
# Download (recursive chart dependencies) with hack script
hack/helm-dependencies.bash

cd charts/umbrella

helm install umbrella . --namespace umbrella --create-namespace
```

## Uninstalling

To teardown your setup, run:

```shell
helm delete umbrella --namespace umbrella
```

## How to contribute

Before contributing, make sure, you read and understood our [contributing guidelines](./CONTRIBUTING.md).
We appreciate every contribution, be it bug reports, feature requests, test automation or enhancements to the Chart(s),
but please keep the following in mind:

- Avoid company specific setup
- Avoid any tooling/infra components, that requires a subscription in any form
- Be vendor and cloud agnostic
