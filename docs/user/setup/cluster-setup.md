# Cluster Setup

This guide provides instructions to set up a Kubernetes cluster required for running the Umbrella Chart.

## System Requirements

| CPU (Cores) | Memory (GB) |
| :----------:| :----------:|
|      4      |      6      |

The above specifications are the minimum requirements for a local development setup. Adjust resources based on your workload for larger or production environments.

## Supported Platforms

### 1. Linux & Mac

> **Note**
> As already mentioned, this is the recommondation, since these two variants are the most tested ones.

Start a Minikube cluster with the following command:
```bash
minikube start --cpus=4 --memory=6gb
```

### 2. Windows

For DNS resolution to work correctly on Windows, you have two options:

#### Option 1: Use the Hyper-V Driver

Start Minikube with administrator privileges using the `--driver=hyperv` flag:
```bash
minikube start --cpus=4 --memory=6gb --driver=hyperv
```

#### Option 2: Use Docker Desktop Kubernetes

Alternatively, you can use the native Kubernetes cluster provided by Docker Desktop:

1. Enable Kubernetes in Docker Desktop:
    - Navigate to **Settings > Kubernetes** and enable the Kubernetes option.

2. Install an NGINX Ingress Controller:
   ```bash
   helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
   ```

3. Use `127.0.0.1` as the Cluster IP and manually configure ingress.

> :warning: The rest of the tutorial assumes a minikube cluster, however.

## Verifying the Cluster

After starting Minikube or Docker Desktop Kubernetes, verify the cluster setup:

- Check that your cluster is running:
  ```bash
  kubectl cluster-info
  ```

- Open the Minikube dashboard to monitor resources:
  ```bash
  minikube dashboard
  ```

## Recommendations

Use tools like [Open Lens](https://k8slens.dev/) or the Minikube dashboard to visualize your cluster and deployed components.

For networking setup, proceed to the [Network Setup Guide](network-setup).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
