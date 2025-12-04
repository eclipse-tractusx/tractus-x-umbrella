# Troubleshooting Guide

This guide provides solutions to common issues encountered during the deployment and operation of the Umbrella Chart.

## Table of Contents

- [Common Issues](#common-issues)
  - [DNS resolution fails due to resolution timeouts](#dns-resolution-fails-due-to-resolution-timeouts)
  - [Digital Twin Registry Ingress and Path Handling](#digital-twin-registry-ingress-and-path-handling)
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

3. Using `vim`, `nano` or any other text editor, open the `/etc/umbrella.resolv.conf` file and **comment out the "search"** line. Save the file. Exit Minikube console.

   ```shell
   vim /etc/umbrella.resolv.conf
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

### Digital Twin Registry Ingress and Path Handling

**Problem symptoms**

- Issues with Ingress and path handling for the Digital Twin Registry.
- Errors when accessing the registry or submodel server.
- Error message during installation: `Error: INSTALLATION FAILED: failed to create resource: admission webhook "validate.nginx.ingress.kubernetes.io" denied the request: ingress contains invalid paths: path /semantics/registry(/|$)(.*) cannot be used with pathType Prefix`

**Solution**

If you encounter problems with Ingress and path handling, you may need to uncomment specific lines in your `values.yaml` file.

Locate the `digital-twin-bundle` configuration in your `values.yaml` and uncomment the following lines under `digital-twin-registry`:

```yaml
    digital-twin-registry:
      registry:
        # UNCOMMENT THE FOLLOWING LINES TO FIX PROBLEMS WITH INGRESS AND PATH HANDLING
        ingress:
          # disable urlPrefix behaviour (that appends a regex to the path)
          urlPrefix: ""
          # provide explicit rules so we can set pathType to ImplementationSpecific
          rules:
            - host: dataprovider-dtr.tx.test
              http:
                paths:
                  - path: "/semantics/registry(/|$)(.*)"
                    pathType: ImplementationSpecific
          className: "nginx"
          annotations:
            cert-manager.io/cluster-issuer: "my-ca-issuer"
            nginx.ingress.kubernetes.io/rewrite-target: "/$2"
            nginx.ingress.kubernetes.io/use-regex: "true"
```

## Linux Issues

*No specific issues documented yet.*

## Windows Issues

*No specific issues documented yet.*

## macOS Issues

*No specific issues documented yet.*
