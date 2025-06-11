# Migration of ingress from http-addon to webapprouting:
Switching to webapprouting means we can no longer use the auto generated domain name by azure. 

The domain name `arena2036-x.de` was already registered in strato and the same was used for webapprouting.

## Steps
### DNS Zone creation
We first create a DNS zone in azure with the name `arena2036-x.de`.  This can be done either via cli or UI.
 
`az network dns zone create --resource-group <ResourceGroupName> --name <ZoneName>` 

### DNS delegation
We have now created a DNS zone in azure. Azure doesn't do any name registration which is why we use the existing name registered under strato in here. 
At this point any lookup on the name `arena2036-x.de` would be pointing to the nameservers defined by strato and the request is never coming to azure. So we have to replace the nameservers defined by strato to custom ones. These are the nameservers of `arena2036-x.de` in azure dns zone.  

Eg: 
```
ns.azure-dns.com.
ns.azure-dns.net.
ns-.azure-dns.org.
ns-.azure-dns.info.
```
To replace the nameservers

- login to strato, select the domain `arena2036-x.de` and click manage domains.

![Image](https://github.com/user-attachments/assets/711831f5-9495-4162-8453-0a11671121be)
- Go to DNS tab and click on manage NS records.

![Image](https://github.com/user-attachments/assets/6456f89c-6875-4e8e-92c1-dabdaa25b462)

- Copy all the 4 NS from azure DNS records to strato.

![Image](https://github.com/user-attachments/assets/28c3d721-9216-4a87-bef8-67e9edea7ba9)
Click on Save. 

**The sync of the nameservers to the new ones takes about 24 hours.**
 
We can verify by checking the output of nslookup.
![Image](https://github.com/user-attachments/assets/a6853b3a-76aa-40b8-8dd6-b3c9d85082b0)

### Enable App routing.
In the azure kubernetes cluster, we enable app routing.
`az aks approuting enable --resource-group <ResourceGroupName> --name <ClusterName>`

### Attach Azure DNS zone to the application routing add-on
Attach the DNS zone created earlier to approuting. 
`ZONEID=$(az network dns zone show --resource-group <ResourceGroupName> --name <ZoneName> --query "id" --output tsv)`
`az aks approuting zone add --resource-group <ResourceGroupName> --name <ClusterName> --ids=${ZONEID} --attach-zones`

### Deploying cert-manager
Deploy cert-manager in the cert-manager namespace. cert-manager is responsible for automating the process of obtaining and renewing SSL/TLS certificates from Let's Encrypt.

```
helm repo add jetstack https://charts.jetstack.io
helm repo update
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.11.0/cert-manager.crds.yaml
```
```
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace
```

### Install ClusterIssuer 
Cluster issuer has the ACME endpoint of letsencrypt and the ingress class that is being used in azure `webapprouting.kubernetes.azure.com` 

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: <email>
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: webapprouting.kubernetes.azure.com
```
```
kubectl apply -f cluster-issuer.yaml
```

### Deploy the Ingress with tls
Add the following config to the ingress yaml 

- `cert-manager.io/cluster-issuer: letsencrypt-prod` in annotations
- `secretName: "<app-name>-tls"` secret name

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: store-front
  namespace: aks-store
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: webapprouting.kubernetes.azure.com
  rules:
  - host: app-test.arena2036-x.de
    http:
      paths:
      - backend:
          service:
            name: store-front
            port:
              number: 80
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - app-test.arena2036-x.de
    secretName: store-front-tls

```

### Enable DNS contributor role for webapprouting module.
webapprouting module needs to be provided with the contributor access so that external-dns has permissions to edit the A-records when ingress configurations are updated.
- Go to Azure DNS and select `arena2036-x.de`
- Select IAM and click on `add` roles

![Image](https://github.com/user-attachments/assets/c8252f7c-4c31-4a05-aa1d-7c168f9aee89)
- Select DNS zone contributor

![Image](https://github.com/user-attachments/assets/090d5e2f-b0af-42e7-adb3-afc4c5c1f94b)
- Select web app routing as the member 

![Image](https://github.com/user-attachments/assets/32793dea-eced-45cf-bd56-3acaebb57b38)
- Click on review and assign

New configurations in ingress are reflected in the DNS records in 3 mins. 
