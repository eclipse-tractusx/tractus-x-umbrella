# Local Installation of Helm Charts and Prerequisites

In order to install the Helm Charts you first need to follow the Cluster installation steps.

Running the helm charts **requires** a kubernetes cluster (`>1.24.x`), it's recommended to run it on [**Minikube**](https://minikube.sigs.k8s.io/docs/start/).
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following instructions to install the chart as `umbrella` release.

After Installing the Charts you probably want to follow the [Network Configuration Step](network/README.md) to make the cluster available on your local machine, for easier access to the services.

## Required versions: 

* Kubernetes version >1.24.x
* Helm version 3.8+

## Installation

1. [Install Cluster](cluster/README.md)
2. [Install Charts](chart-installation/README.md)
   1. [Released Charts](chart-installation/released-chart.md)
   2. [Local Charts](chart-installation/local-repository.md)
   3. [Uninstallation](chart-installation/uninstallation.md)
3. [Network Configuration](network/README.md)
   1. [TLS (Optional)](network/tls.md)
4. [Semantic Hub Precondition](semantic-hub/README.md)