# Network Setup

This guide provides instructions to configure the network setup required for running the Umbrella Chart in a Kubernetes cluster.

## Enable Ingress

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
   - [IATP Mock](http://iatpmock.tx.test)
   - [pgAdmin4](http://pgadmin4.tx.test)
   - [SSI DIM Wallet Stub](http://ssi-dim-wallet-stub.tx.test)

## DNS Resolution Setup

Proper DNS resolution is required to map local domain names to the Minikube IP address. Follow the steps for your operating system:

- [Linus](#linux)
- [mac](#macos)
  - [using Minikube](#option-1-minikube)
  - [using K3s](#option-2-k3s)
- [Windows](#windows)

### Linux

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

      See https://linux.die.net/man/5/resolver for more information.

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

      If you still face DNS issues, add [the hosts](#hosts-file-configuration-fallback) to your `/etc/hosts` file.

3. Test DNS resolution by pinging one of the configured hostnames.

### macOS

Please refer to [option 1](#option-1-minikube) for the dns setup in case you're using Minikube, which is the most tested and therefore the recommended option.
[Option 2](#option-2-k3s) outlines the dns setup in case you're using K3s.

#### Option 1: Minikube

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

   If you still face DNS issues, add [the hosts](#hosts-file-configuration-fallback) to your `/etc/hosts` file.

2. Additional network setup for macOS

   Install and start [Docker Mac Net Connect](https://github.com/chipmk/docker-mac-net-connect#installation).

   We also recommend to execute the usage example after install to check proper setup.

3. Test DNS resolution by pinging one of the configured hostnames.

#### Option 2: K3s

Here the easiest solution is the configuration via hosts:

1. add [the hosts](#hosts-file-configuration-fallback) to your `/etc/hosts` file of your **Mac**, use `127.0.0.1` to replace the placeholder `<MINIKUBE_IP>`

2. add [the hosts](#hosts-file-configuration-fallback) to your `/etc/hosts` file of your **lima vm**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

   ```bash
   #to login to your limavm
   limactl shell k3s
   ```

3. add [the hosts](#hosts-file-configuration-fallback) to your coredns configuration of your **k3s-cluster**, use `192.168.5.15` to replace the placeholder `<MINIKUBE_IP>`

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
4. Test DNS resolution by pinging one of the configured hostnames.

### Windows

1. Open PowerShell as Administrator.
2. Add a DNS client rule for `.test` domains:
   ```bash
   Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

   The following will remove any matching rules before creating a new one. This is useful for updating the minikube ip.
   ```shell
   Get-DnsClientNrptRule | Where-Object {$_.Namespace -eq '.test'} | Remove-DnsClientNrptRule -Force; Add-DnsClientNrptRule -Namespace ".test" -NameServers "$(minikube ip)"
   ```

   If you still face DNS issues, add [the hosts](#hosts-file-configuration-fallback) to your `C:\Windows\System32\drivers\etc\hosts` file.

3. Test DNS resolution by pinging one of the configured hostnames.

---

## Hosts File Configuration (Fallback)

If DNS resolution does not work, update the `/etc/hosts` (Linux/macOS) or `C:\Windows\System32\drivers\etc\hosts` (Windows) file with the following entries:

```
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
<MINIKUBE_IP>    iatpmock.tx.test
<MINIKUBE_IP>    business-partners.tx.test
<MINIKUBE_IP>    pgadmin4.tx.test
<MINIKUBE_IP>    ssi-dim-wallet-stub.tx.test
```

Replace `<MINIKUBE_IP>` with the output of the following command:
```bash
minikube ip
```

## Verify Network Setup

Once the DNS resolution or hosts file is configured:
1. Ensure ingress is working by accessing a service endpoint, such as:
   ```
   http://portal.tx.test
   ```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
