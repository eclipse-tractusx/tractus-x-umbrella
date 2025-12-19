# Troubleshooting Guide

This guide provides solutions to common issues encountered during the deployment and operation of the Umbrella Chart.

## Table of Contents

- [Common Issues](#common-issues)
  - [DNS resolution fails due to resolution timeouts](#dns-resolution-fails-due-to-resolution-timeouts)
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
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

