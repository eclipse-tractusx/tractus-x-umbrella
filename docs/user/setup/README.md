# Cluster Setup

This guide provides instructions to set up a Kubernetes cluster required for running the Umbrella Chart.

## System Requirements

| CPU (Cores) | Memory (GB) |
| :----------:| :----------:|
|      4      |      6      |

The above specifications are the minimum requirements for a local development setup. Adjust resources based on your workload for larger or production environments.

## Supported Platforms

> **Note**
> It is recommended to use Linux or macOS because those two are the most tested platforms with the umbrella.

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

- [Linux](#1-linux)
- [macOS](#2-macos)
  - [using Minikube with Docker Desktop](#option-1-docker-desktop-available)
  - [using K3s with lima](#option-2-no-docker-desktop-available)
- [Windows](#3-windows)

### 1. Linux

Start a Minikube cluster with the following command:

```bash
minikube start --cpus=4 --memory=6gb
```

### 2. macOS

Please refer to [option 1](#option-1-docker-desktop-available) with Minikube for the cluster setup in case you're using Docker Desktop, which is the most tested and therefore the recommended option.
[Option 2](#option-2-no-docker-desktop-available) outlines [lima](https://lima-vm.io/) with K3s as cluster option in case Docker Desktop isn't available.

#### Option 1: Docker Desktop available

Start a Minikube cluster with the following command:

```bash
minikube start --cpus=4 --memory=6gb
```

#### Option 2: No docker desktop available

In this case, a tested way to setup your local kubernetes cluster is with [lima](https://lima-vm.io/) and [K3s](https://k3s.io/):

```bash
brew install lima

#as we are using a vm template, we download it first
curl -O https://raw.githubusercontent.com/lima-vm/lima/refs/heads/master/templates/k3s.yaml
```

then we need to modify it a little, to propagate your proxysettings, add the following:

```yaml
propagateProxyEnv: true
```

if you for example need ca-certificates because of a corporate proxy then add the following:

```yaml
caCerts:
  removeDefaults: null
  files:
  - /path/to/your/certificates/ca-certificates.crt
```

to adjust the size of your vm add:

```yaml
cpus: 6
memory: 8GiB
```

to support also non-arm images in your cluster add:

```yaml
rosetta:
  enabled: true
  binfmt: true
vmType: vz
```

as K3s comes with traefik by default and these helm charts are for NGINX ingress, we need to modify the install script (starting line 39) a [little](https://www.suse.com/support/kb/doc/?id=000020082):

```yaml
- mode: system
  script: |
    #!/bin/bash
    set -eux -o pipefail
    export K3S_KUBECONFIG_MODE="644"
    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik" sudo sh -
    cat >/var/lib/rancher/k3s/server/manifests/ingress-nginx.yaml <<EOF
    apiVersion: v1
    kind: Namespace
    metadata:
      name: ingress-nginx
    ---
    apiVersion: helm.cattle.io/v1
    kind: HelmChart
    metadata:
      name: ingress-nginx
      namespace: kube-system
    spec:
      chart: ingress-nginx
      repo: https://kubernetes.github.io/ingress-nginx
      targetNamespace: ingress-nginx
      version: v4.11.2
      set:
      valuesContent: |-
        fullnameOverride: ingress-nginx
        controller:
          kind: DaemonSet
          hostNetwork: true
          hostPort:
            enabled: true
          service:
            enabled: false
          publishService:
            enabled: false
          metrics:
            enabled: true
            serviceMonitor:
              enabled: false
          config:
            use-forwarded-headers: "true"
    EOF
```

after this you can start your vm:

```bash
#prepare no_proxy for the testdomains
export no_proxy=$no_proxy,192.168.5.15,.test

#start the vm
limactl start k3s.yaml

#configure kubectl
export KUBECONFIG="/Users/YOURUSER/.lima/docker/copied-from-guest/kubeconfig.yaml"
```

### 3. Windows

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

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

Use tools like the Minikube dashboard (or [Open Lens](https://k8slens.dev/)) to visualize your cluster and deployed components.

For networking setup, proceed to the [Network Setup Guide](../network/README.md).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
