# Network Setup

This guide provides instructions to configure the network setup required for running the Umbrella Chart in a Kubernetes cluster.

## Enabled Ingresses

To enable ingress for local access, use the following command with Minikube:

```bash
minikube addons enable ingress
```

Make sure that the **DNS** resolution for the hosts is in place:

```bash
minikube addons enable ingress-dns
```

And execute installation step [3 Add the `minikube ip` as a DNS server](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns) for your OS

### Enable Ingress

The following ingresses are configured and available:

- **Authentication Services**
  - [CentralIdP](http://centralidp.tx.test/auth/)
  - [SharedIdP](http://sharedidp.tx.test/auth/)

- **Portal Services**
  - [Portal Frontend](http://portal.tx.test)
  - [Portal Backend](http://portal-backend.tx.test)
    - [Administration API](http://portal-backend.tx.test/api/administration/swagger/index.html)
    - [Registration API](http://portal-backend.tx.test/api/registration/swagger/index.html)
    - [Apps API](http://portal-backend.tx.test/api/apps/swagger/index.html)
    - [Services API](http://portal-backend.tx.test/api/services/swagger/index.html)
    - [Notification API](http://portal-backend.tx.test/api/notification/swagger/index.html)

- **Discovery**
  - [Discovery Finder API](http://semantics.tx.test/discoveryfinder/swagger-ui/index.html)

- **Data Exchange Services**
  - [Data Consumer 1 Control Plane](http://dataconsumer-1-controlplane.tx.test)
  - [Data Consumer 1 Data Plane](http://dataconsumer-1-dataplane.tx.test)
  - [Data Provider Data Plane](http://dataprovider-dataplane.tx.test)
  - [Data Consumer 2 Control Plane](http://dataconsumer-2-controlplane.tx.test)
  - [Data Consumer 2 Data Plane](http://dataconsumer-2-dataplane.tx.test)

- **Additional Services**
  - [Business Partners Pool](http://business-partners.tx.test/pool)
  - [Business Partners Orchestrator](http://business-partners.tx.test/orchestrator)
  - [BDRS Server](http://bdrs-server.tx.test)
  - [SSI Credential Issuer](http://ssi-credential-issuer.tx.test/api/issuer/swagger/index.html)
  - [SSI DIM Wallet Stub](http://ssi-dim-wallet-stub.tx.test)
  - [pgAdmin4](http://pgadmin4.tx.test)

## DNS Resolution Setup

Proper DNS resolution is required to map local domain names to the Minikube IP address. There are different ways to configure DNS. The most reliable way is to adapt the [hosts file configuration](#hosts-file-configuration) on your system. [Here](#alternative-approaches), you find alternative approaches  for the resolution setup.

### Hosts File Configuration

For this approach you have to insert new entries to your hosts file.  
> **Note**
> There are two things to consider here.
> Firstly, the existing entries should not be changed.
> Secondly, the adjustments made should be undone when the tutorial is no longer needed.

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

Below you will find the different procedures for [Linux using minikube](#linux-using-minikube), [macOS using minikube](#macos-using-minikube), [macOS using  K3s](#macos-using-k3s) and [Windows](#windows).

The following values need to be added in each case:

   ```text
   <MINIKUBE_IP>    centralidp.tx.test
   <MINIKUBE_IP>    sharedidp.tx.test
   <MINIKUBE_IP>    portal.tx.test
   <MINIKUBE_IP>    portal-backend.tx.test
   <MINIKUBE_IP>    semantics.tx.test
   <MINIKUBE_IP>    sdfactory.tx.test
   <MINIKUBE_IP>    ssi-credential-issuer.tx.test
   <MINIKUBE_IP>    dataconsumer-1-dataplane.tx.test
   <MINIKUBE_IP>    dataconsumer-1-controlplane.tx.test
   <MINIKUBE_IP>    dataprovider-dataplane.tx.test
   <MINIKUBE_IP>    dataprovider-controlplane.tx.test
   <MINIKUBE_IP>    dataprovider-submodelserver.tx.test
   <MINIKUBE_IP>    dataconsumer-2-dataplane.tx.test
   <MINIKUBE_IP>    dataconsumer-2-controlplane.tx.test
   <MINIKUBE_IP>    bdrs-server.tx.test
   <MINIKUBE_IP>    business-partners.tx.test
   <MINIKUBE_IP>    pgadmin4.tx.test
   <MINIKUBE_IP>    ssi-dim-wallet-stub.tx.test
   <MINIKUBE_IP>    smtp.tx.test
   ```

#### Linux using minikube

   1. Open the hosts file you find here `/etc/hosts` and insert the values from above.

   2. Replace `<MINIKUBE_IP>` with the output of the following command:

      ```bash
         minikube ip
      ```

   3. Test DNS resolution by pinging one of the configured hostnames.

#### macOS using minikube

   1. Open the hosts file you find here: `/etc/hosts` and insert the values from above.

   2. Replace `<MINIKUBE_IP>` with the output of the following command:

      ```bash
         minikube ip
      ```

   3. Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

      We recommend to execute the usage example that can be found there after installation to check proper setup.

   4. Test DNS resolution by pinging one of the configured hostnames.

#### macOS using K3s

1. Add the values from above to your `/etc/hosts` file of your **Mac**, use `127.0.0.1` to replace the placeholder `<MINIKUBE_IP>`

2. Add the values from above to your `/etc/hosts` file of your **lima vm**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

   ```bash
   #to login to your limavm
   limactl shell k3s
   ```

3. Add the values from aboveto your coredns configuration of your **k3s-cluster**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

   ```bash
   kubectl edit cm coredns -n kube-system
   ```

   ```yaml
   apiVersion: v1
   data:
   Corefile: |
      .:53 {
         log
         errors
         health
         ready
         kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
         }
         hosts /etc/coredns/NodeHosts {
            #ADD THE HOSTS HERE
            ttl 60
            reload 15s
            fallthrough
         }
   ```

   > **Note**
   > If you do this step, after you already deployed the helm charts, make sure to  restart your java backend pods (controlplane and dataplane) to refresh their dns resolution.
   > To make this change permanent in your vm, make sure to update `/var/lib/rancher/k3s/server/manifests/coredns.yaml` in the install script of your vm template

3. Test DNS resolution by pinging one of the configured hostnames.

   #### Windows

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

   1. Open the hosts file you find here: `C:\Windows\System32\drivers\etc\hosts` and insert the values from above.

   2. Replace `<MINIKUBE_IP>` with the output of the following command:

      ```bash
         minikube ip
      ```

   3. Test DNS resolution by pinging one of the configured hostnames.

### Alternative approaches

Below you find alternative approaches for setting the DNS resolution. Follow the steps for your operating system:

- [Linux](#linux)
- [macOS using Minikube](#macos-using-minikube-1)
- [Windows](#windows-alternative)

#### Linux

1. Identify your DNS resolver by checking the contents of `/etc/resolv.conf`.
2. Update the resolver configuration based on your system:

    - **resolvconf**:
      Add the following to `/etc/resolvconf/resolv.conf.d/base`:

      ```bash
      search test
      nameserver $(minikube ip)
      timeout 5
      ```

      If your Linux OS uses `systemctl`, run the following commands:

      ```bash
      sudo resolvconf -u
      systemctl disable --now resolvconf.service
      ```

      See <https://linux.die.net/man/5/resolver> for more information.

    - **NetworkManager**:
      NetworkManager can run integrated caching DNS server - `dnsmasq` plugin and can be configured to use separate nameservers per domain.

      Edit `/etc/NetworkManager/NetworkManager.conf` and enable `dns=dnsmasq` by adding:

      ```bash
      [main]
      dns=dnsmasq
      ```

      Also see `dns=` in [NetworkManager.conf](https://developer.gnome.org/NetworkManager/stable/NetworkManager.conf.html).

      Configure dnsmasq to handle domain names ending with `.test`:

      ```bash
      sudo mkdir -p /etc/NetworkManager/dnsmasq.d/
      echo "server=/test/$(minikube ip)" | sudo tee /etc/NetworkManager/dnsmasq.d/minikube.conf
      ```

      Restart NetworkManager:

      ```bash
      systemctl restart NetworkManager.service
      ```

      Ensure your `/etc/resolv.conf` contains only single nameserver:

      ```bash
      cat /etc/resolv.conf | grep nameserver
      nameserver 127.0.0.1
      ```

    - **systemd-resolved**:
      Run the following commands to add the minikube DNS for `.test` domains:

      ```bash
      sudo mkdir -p /etc/systemd/resolved.conf.d
      sudo tee /etc/systemd/resolved.conf.d/minikube.conf << EOF
      [Resolve]
      DNS=$(minikube ip)
      Domains=~test
      EOF
      sudo systemctl restart systemd-resolved
      ```

3. Test DNS resolution by pinging one of the configured hostnames.

#### macOS using Minikube

Please refer to the following instructions for the dns setup in case you're using Minikube, which is the most tested and therefore the recommended option.

1. Create a resolver configuration for `.test` domains:

   ```bash
   sudo mkdir -p /etc/resolver
   sudo bash -c "echo 'nameserver $(minikube ip)' > /etc/resolver/test"
   ```

   and also add these lines to `/etc/resolver/test`:

   ```bash
   domain tx.test
   search_order 1
   timeout 5
   ```

2. Additional network setup for macOS

   Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

   We recommend to execute the usage example that can be found there after installation to check proper setup.

3. Test DNS resolution by pinging one of the configured hostnames.

#### Windows alternative

> [!WARNING]
> As we do not currently test on Windows, we would greatly appreciate any contributions from those who successfully deploy it on Windows.

1. Open PowerShell as Administrator.
2. Add a DNS client rule for `.test` domains:

   ```bash
   Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

   The following will remove any matching rules before creating a new one. This is useful for updating the minikube ip.

   ```shell
   Get-DnsClientNrptRule | Where-Object {$_.Namespace -eq '.test'} | Remove-DnsClientNrptRule -Force; Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

3. Test DNS resolution by pinging one of the configured hostnames.

---

## Verify Network Setup

Once the DNS resolution or hosts file is configured:

1. Ensure ingress is working by accessing a service endpoint, such as <http://portal.tx.test>

---

## Troubleshooting

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

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
