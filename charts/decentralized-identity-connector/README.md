# Dataprovider Helm Chart

This chart includes EDC, Digital Twin Registry and a Submodel Server.  
The Submodel Server images is based on an older Catena-X demo (catenax at home) since this is what we were using in our
testing environments.

## Prerequisites

- Running Kubernetes cluster
- Helm is installed

Example for local usage:

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Minikube ingress addon](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns/)

## Installing

Run the Chart with

```shell
helm dependency update
helm install decentralized-edc . --timeout 10m0s
```

Remove the chart by running

```shell
helm uninstall decentralized-edc
```
## Configuration

For the main shared configuration between identityhub and connector, fill the `shared-configuration` in values.yaml.

Configuration of EDC + Digital Twin + Simple Data Backend see [tractus-x-umbrella/tree/main/charts/tx-data-provider](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/charts/tx-data-provider)

Configuration of IdentityHub see [tractusx-identityhub/tree/main/charts/tractusx-identityhub](https://github.com/eclipse-tractusx/tractusx-identityhub/tree/main/charts/tractusx-identityhub)
