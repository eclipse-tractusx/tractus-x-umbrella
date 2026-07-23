# Troubleshooting Guide

This guide provides solutions to common issues encountered during the deployment and operation of the Umbrella Chart.

## Table of Contents

- [Common Issues](#common-issues)
  - [DNS resolution fails due to resolution timeouts](#dns-resolution-fails-due-to-resolution-timeouts)
  - [CentralIDP and SharedIDP pods enter CrashLoopBackOff during startup](#centralidp-and-sharedidp-pods-enter-crashloopbackoff-during-startup)
- [Linux Issues](#linux-issues)
- [Windows Issues](#windows-issues)
- [macOS Issues](#macos-issues)

## Common Issues

### DNS resolution fails due to resolution timeouts

**Problem background**

Minikube node DNS settings are inherited from the configuration specified in the `/etc/resolv.conf` file on the host where Minikube is running. This particularly applies to the search field in the `resolv.conf` file.
The values defined in the search field are propagated to individual pods within the cluster. 

The search field contains a list of domain suffixes that are appended to queried domain names. 
These modified domain names are then sequentially resolved by the DNS server.

In certain circumstances, this mechanism can lead to issues such as domain name resolution timeouts.

**Problem symptoms**

- umbrella-dataprovider-post-install-testdata-...  pod fails
- It is not possible to query DSP catalog because of the HTTP 500 ERROR. 
- When looking into umbrella-dataconsumer-1-edc-controlplane logs, there are this kind of error messages:

   ```text
   HTTP client exception caught for request [POST, http://ssi-dim-wallet-stub.tx.test/oauth/token]
   org.eclipse.edc.http.spi.EdcHttpClientException: ssi-dim-wallet-stub.tx.test: Try again
   ```

- There are some timeout errors related to domain names resolution in CoreDns log:

   ```text
   [ERROR] plugin/errors: 2 ssi-dim-wallet-stub.tx.test.some-domain.com. A: read udp 10.244.1.154:36890->8.8.8.8:53: i/o timeout
   [ERROR] plugin/errors: 2 ssi-dim-wallet-stub.tx.test.some-domain.com. AAAA: read udp 10.244.1.154:35576->8.8.8.8:53: i/o timeout
   ```

- When trying to ping any domain from inside any pod in the cluster, domain name resolution fails or gets timeout. Adding a dot (for example `google.com.`) at the end of the domain fixes the issue.

**Solution**

Prevent pods from inheriting `/etc/resolv.conf` search field values from the Minikube node.

1. Log into Minikube node, using `ssh`.

   ```bash
   minikube ssh
   ```

   In the Minikube node, install any text editor, for example vim:

   ```bash
   sudo apt update && apt install vim
   ```
 
2. While still in the Minikube node console, duplicate existing `/etc/resolv.conf` file, for example:

   ```shell
   cp /etc/resolv.conf  /etc/umbrella.resolv.conf
   ```

3. Using `vim`, `nano` or any other text editor, open the `/etc/umbrella.resolv.conf` file.

   ```shell
   vim /etc/umbrella.resolv.conf
   ```

   **Comment out the "search" line** (add a `#` at the beginning of the line). It should look like this:

   ```text
   nameserver 10.0.2.3
   # search .
   ```

   Save the file and exit the Minikube console.

   ```shell
   exit
   ```

4. Stop the Minikube and start it again appending the following flag to Minikube startup command:
   
   ```text
   --extra-config=kubelet.resolv-conf="/etc/umbrella.resolv.conf"
   ```
      
   So the final Minikube startup command will look like this:

   ```shell
   minikube start --cpus=4 --memory=6gb --extra-config=kubelet.resolv-conf="/etc/umbrella.resolv.conf"
   ```

<<<<<<< Updated upstream
### Portal pods fail to start in resource-constrained local environments

**Problem background**

When deploying the Portal on local Kubernetes environments such as Minikube, the available CPU and memory resources may not be sufficient for the Portal components.

By default, the `values.yaml` file does not include a recommended resource configuration for these environments. As a result, Portal pods may fail to start because Kubernetes cannot allocate enough resources.

Providing explicit resource requests and limits resolves the issue, but users may not immediately recognize that insufficient resources are the root cause.

**Problem symptoms**

- One or more Portal pods remain in the `Pending` or `CrashLoopBackOff` state.
- The Portal application is not accessible after deployment.
- Pod events indicate insufficient memory or CPU resources.
- Increasing the resource requests and limits allows the Portal to start successfully.

**Solution**

Configure resource requests and limits for the Portal.

1. Open the `values.yaml` file.

2. Locate the `portal` section and uncomment the following resource configuration:

   ```yaml
portal:
  enabled: false
  replicaCount: 1
  # Uncomment this section if the Portal pods fail to start in 
  # resource-constrained local environments due to insufficient memory.
  centralidp:
    realmSeeding:
      resources:
        requests:
          memory: "512Mi"
        limits:
          memory: "1Gi"

  sharedidp:
    realmSeeding:
      resources:
        requests:
          memory: "512Mi"
        limits:
          memory: "1Gi"
   ```

   Alternatively, if the chart already contains the commented example, simply uncomment it:

   ```yaml
   # Uncomment this section if the Portal pods fail to start in
   # resource-constrained local environments due to insufficient memory.
   #
   # resources:
   #   limits:
   #     memory: 2Gi
   #     cpu: 1000m
   #   requests:
   #     memory: 1Gi
   #     cpu: 500m
   ```

3. Redeploy or upgrade the Helm release.

   ```bash
   helm upgrade --install umbrella ./umbrella -f values.yaml
   ```

4. Verify that the Portal pods are running successfully.

   ```bash
   kubectl get pods
   ```

   The Portal pods should now reach the `Running` state.
=======
### CentralIDP and SharedIDP pods enter CrashLoopBackOff during startup

**Problem background**

When deploying the Umbrella Chart on resource-constrained local Kubernetes environments such as Minikube, the `centralidp` and `sharedidp` pods may repeatedly fail during startup and enter the `CrashLoopBackOff` state.

The root cause is the Keycloak cache, which is enabled by default. During the initial startup, cache initialization significantly increases memory consumption. As a result, the application may not become ready before the configured startup probes fail, causing Kubernetes to restart the containers. In some cases, the process is terminated by the operating system due to insufficient memory.

Disabling the Keycloak cache reduces the startup memory requirements and allows the deployment to complete successfully in local environments.

**Problem symptoms**

- `centralidp` pod enters the `CrashLoopBackOff` state.
- `sharedidp` pod enters the `CrashLoopBackOff` state.
- The deployment does not complete successfully.
- Pod logs or events may contain messages indicating that the process was terminated (`Killed`) due to excessive memory usage.
- The readiness or liveness probes repeatedly fail during startup.

**Solution**

Disable the Keycloak cache for both CentralIDP and SharedIDP when deploying on local Minikube environments.

Deploy the Umbrella Chart with the following Helm flags:

```bash
helm upgrade --install umbrella . \
  -f values-adopter-portal.yaml \
  --set centralidp.keycloak.cache.enabled=false \
  --set sharedidp.keycloak.cache.enabled=false \
  --namespace umbrella \
  --create-namespace
```

Alternatively, disable the cache in your `values.yaml` file:

```yaml
centralidp:
  keycloak:
    cache:
      enabled: false

sharedidp:
  keycloak:
    cache:
      enabled: false
```

After redeploying with the cache disabled, verify that the pods reach the `Running` state:

```bash
kubectl get pods
```

Both `centralidp` and `sharedidp` should start successfully and the Portal deployment should complete.
>>>>>>> Stashed changes

## Linux Issues

*No specific issues documented yet.*

## Windows Issues

*No specific issues documented yet.*

## macOS Issues

*No specific issues documented yet.*

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* SPDX-FileCopyrightText: 2026 LKS Next
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

