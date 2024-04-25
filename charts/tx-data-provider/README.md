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
helm install dataprovider . --timeout 10m0s
```

Remove the chart by running

```shell
helm uninstall dataprovider
```
## Configuration

For Configuration of digital twin registry see [sldt-digital-twin-registry/tree/main/charts/registry](https://github.com/eclipse-tractusx/sldt-digital-twin-registry/tree/main/charts/registry)

Configuration of EDC see [tractusx-edc/tree/main/charts/tractusx-connecto](https://github.com/eclipse-tractusx/tractusx-edc/tree/main/charts/tractusx-connector)

EDC requires connection to HashiCorp Vault and Manage Identity Wallet. These have to be configured for the dataprovider to be operative. 

The Chart can be used as dataprovider by setting `simple-data-backend.enabled`, `digital-twin-registry.enabled` and `seedTestdata` to `false`.

## Testdata seeding

After the installation, a Post-Install Helm Hook will be started which initiates the seeding of testdata. The Hook executes a python script which uploads a provided test dataset to the dataprovider. Documentation to the python script can be found here [README](https://github.com/eclipse-tractusx/item-relationship-service/blob/main/local/testing/testdata/README.md)

Test data set and upload script are stored in [resources/](resources) and provided to the hook as config map.  
A custom config map can be used to provided e.g. `testdataConfigMap: my-custom-testdata-configmap`.