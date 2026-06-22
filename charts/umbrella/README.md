# Umbrella Chart

![Version: 3.16.0](https://img.shields.io/badge/Version-3.16.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

A Helm chart to spin up Tractus-X OSS components to simulate a complete dataspace network.

With this Helm chart you are able to run end-to-end or create a sandbox environment.

It provides a foundation for running end-to-end tests or creating sandbox environments of the [Catena-X](https://catena-x.net/en/) automotive dataspace using [Eclipse Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) OSS components.

## Source Code

* <https://github.com/eclipse-tractusx/tractus-x-umbrella>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| file://../identity-and-trust-bundle | identity-and-trust-bundle | 1.1.3 |
| file://../tx-data-provider | dataconsumerTwo(tx-data-provider) | 0.4.7 |
| file://../tx-data-provider | dataconsumerOne(tx-data-provider) | 0.4.7 |
| file://../tx-data-provider | tx-data-provider | 0.4.7 |
| https://charts.jetstack.io | cert-manager | v1.18.2 |
| https://eclipse-tractusx.github.io/charts/dev | bdrs-server-memory | 0.5.7 |
| https://eclipse-tractusx.github.io/charts/dev | bpdm | 6.3.0 |
| https://eclipse-tractusx.github.io/charts/dev | bpndiscovery | 0.5.1 |
| https://eclipse-tractusx.github.io/charts/dev | centralidp | 4.2.1 |
| https://eclipse-tractusx.github.io/charts/dev | discoveryfinder | 0.5.1 |
| https://eclipse-tractusx.github.io/charts/dev | portal | 2.6.0 |
| https://eclipse-tractusx.github.io/charts/dev | selfdescription(sdfactory) | 2.1.35 |
| https://eclipse-tractusx.github.io/charts/dev | semantic-hub | 0.5.0 |
| https://eclipse-tractusx.github.io/charts/dev | sharedidp | 4.2.1 |
| https://eclipse-tractusx.github.io/charts/dev | ssi-credential-issuer | 1.4.0 |
| https://grafana.github.io/helm-charts | grafana(grafana) | 8.10.1 |
| https://grafana.github.io/helm-charts | loki(loki) | 6.27.0 |
| https://helm.runix.net | pgadmin4 | 1.25.x |
| https://jaegertracing.github.io/helm-charts | jaeger(jaeger) | 3.0.7 |
| https://open-telemetry.github.io/opentelemetry-helm-charts | opentelemetry-collector(opentelemetry-collector) | 0.126.0 |
| https://prometheus-community.github.io/helm-charts | prometheus(prometheus) | 27.1.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| bdrs-server-memory.enabled | bool | `false` |  |
| bdrs-server-memory.fullnameOverride | string | `"bdrs-server"` |  |
| bdrs-server-memory.nameOverride | string | `"bdrs-server"` |  |
| bdrs-server-memory.seeding.bpnList[0].bpn | string | `"BPNL00000003CRHK"` |  |
| bdrs-server-memory.seeding.bpnList[0].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| bdrs-server-memory.seeding.bpnList[10].bpn | string | `"BPNL00000003CML1"` |  |
| bdrs-server-memory.seeding.bpnList[10].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CML1"` |  |
| bdrs-server-memory.seeding.bpnList[11].bpn | string | `"BPNL00000003B2OM"` |  |
| bdrs-server-memory.seeding.bpnList[11].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003B2OM"` |  |
| bdrs-server-memory.seeding.bpnList[12].bpn | string | `"BPNL00000003B0Q0"` |  |
| bdrs-server-memory.seeding.bpnList[12].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003B0Q0"` |  |
| bdrs-server-memory.seeding.bpnList[13].bpn | string | `"BPNL00000003B5MJ"` |  |
| bdrs-server-memory.seeding.bpnList[13].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003B5MJ"` |  |
| bdrs-server-memory.seeding.bpnList[14].bpn | string | `"BPNS0000000008ZZ"` |  |
| bdrs-server-memory.seeding.bpnList[14].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNS0000000008ZZ"` |  |
| bdrs-server-memory.seeding.bpnList[15].bpn | string | `"BPNL00000003CNKC"` |  |
| bdrs-server-memory.seeding.bpnList[15].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CNKC"` |  |
| bdrs-server-memory.seeding.bpnList[16].bpn | string | `"BPNS00000008BDFH"` |  |
| bdrs-server-memory.seeding.bpnList[16].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNS00000008BDFH"` |  |
| bdrs-server-memory.seeding.bpnList[1].bpn | string | `"BPNL00000003B3NX"` |  |
| bdrs-server-memory.seeding.bpnList[1].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003B3NX"` |  |
| bdrs-server-memory.seeding.bpnList[2].bpn | string | `"BPNL00000003CSGV"` |  |
| bdrs-server-memory.seeding.bpnList[2].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CSGV"` |  |
| bdrs-server-memory.seeding.bpnList[3].bpn | string | `"BPNL00000003B6LU"` |  |
| bdrs-server-memory.seeding.bpnList[3].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003B6LU"` |  |
| bdrs-server-memory.seeding.bpnList[4].bpn | string | `"BPNL00000003AXS3"` |  |
| bdrs-server-memory.seeding.bpnList[4].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AXS3"` |  |
| bdrs-server-memory.seeding.bpnList[5].bpn | string | `"BPNL00000003AZQP"` |  |
| bdrs-server-memory.seeding.bpnList[5].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AZQP"` |  |
| bdrs-server-memory.seeding.bpnList[6].bpn | string | `"BPNL00000003AWSS"` |  |
| bdrs-server-memory.seeding.bpnList[6].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AWSS"` |  |
| bdrs-server-memory.seeding.bpnList[7].bpn | string | `"BPNL00000003AYRE"` |  |
| bdrs-server-memory.seeding.bpnList[7].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AYRE"` |  |
| bdrs-server-memory.seeding.bpnList[8].bpn | string | `"BPNL00000003AVTH"` |  |
| bdrs-server-memory.seeding.bpnList[8].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AVTH"` |  |
| bdrs-server-memory.seeding.bpnList[9].bpn | string | `"BPNL00000000BJTL"` |  |
| bdrs-server-memory.seeding.bpnList[9].did | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000000BJTL"` |  |
| bdrs-server-memory.seeding.enabled | bool | `true` |  |
| bdrs-server-memory.seeding.url | string | `"http://bdrs-server:8081"` |  |
| bdrs-server-memory.server.endpoints.management.authKey | string | `"TEST"` |  |
| bdrs-server-memory.server.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| bdrs-server-memory.server.ingresses[0].className | string | `"nginx"` |  |
| bdrs-server-memory.server.ingresses[0].enabled | bool | `true` |  |
| bdrs-server-memory.server.ingresses[0].endpoints[0] | string | `"directory"` |  |
| bdrs-server-memory.server.ingresses[0].endpoints[1] | string | `"management"` |  |
| bdrs-server-memory.server.ingresses[0].hostname | string | `"bdrs-server.tx.test"` |  |
| bdrs-server-memory.server.ingresses[0].tls.enabled | bool | `false` |  |
| bdrs-server-memory.server.trustedIssuers[0] | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| bpdm.bpdm-cleaning-service-dummy.applicationConfig.bpdm.client.orchestrator.base-url | string | `"http://business-partners.tx.test/orchestrator"` |  |
| bpdm.bpdm-cleaning-service-dummy.applicationConfig.bpdm.client.orchestrator.provider.issuer-uri | string | `"http://centralidp.tx.test/auth/realms/CX-Central"` |  |
| bpdm.bpdm-cleaning-service-dummy.applicationConfig.bpdm.client.orchestrator.registration.client-id | string | `"sa-cl25-cx-1"` |  |
| bpdm.bpdm-cleaning-service-dummy.applicationSecrets.bpdm.client.orchestrator.registration.client-secret | string | `"changeme"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.bpn.owner-bpn-l | string | `nil` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.client.orchestrator.base-url | string | `"http://business-partners.tx.test/orchestrator"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.client.orchestrator.registration.client-id | string | `"sa-cl25-cx-3"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.client.pool.base-url | string | `"http://business-partners.tx.test/pool"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.client.pool.registration.client-id | string | `"sa-cl7-cx-1"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.datasource.host | string | `"bpdm-postgres"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.security.auth-server-url | string | `"http://centralidp.tx.test/auth"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.security.client-id | string | `"Cl16-CX-BPDMGate"` |  |
| bpdm.bpdm-gate.applicationConfig.bpdm.security.realm | string | `"CX-Central"` |  |
| bpdm.bpdm-gate.applicationConfig.server.forward-headers-strategy | string | `"FRAMEWORK"` |  |
| bpdm.bpdm-gate.applicationSecrets.bpdm.client.orchestrator.registration.client-secret | string | `"changeme"` |  |
| bpdm.bpdm-gate.applicationSecrets.bpdm.client.pool.registration.client-secret | string | `"changeme"` |  |
| bpdm.bpdm-gate.applicationSecrets.spring.datasource.password | string | `"dbpasswordbpdm"` |  |
| bpdm.bpdm-gate.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| bpdm.bpdm-gate.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| bpdm.bpdm-gate.ingress.annotations."nginx.ingress.kubernetes.io/x-forwarded-prefix" | string | `"/gate"` |  |
| bpdm.bpdm-gate.ingress.enabled | bool | `true` |  |
| bpdm.bpdm-gate.ingress.hosts[0].host | string | `"business-partners.tx.test"` |  |
| bpdm.bpdm-gate.ingress.hosts[0].paths[0].path | string | `"/gate(/|$)(.*)"` |  |
| bpdm.bpdm-gate.ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| bpdm.bpdm-gate.postgres.fullnameOverride | string | `nil` |  |
| bpdm.bpdm-gate.postgres.nameOverride | string | `"bpdm-postgres"` |  |
| bpdm.bpdm-orchestrator.applicationConfig.bpdm.datasource.host | string | `"bpdm-postgres"` |  |
| bpdm.bpdm-orchestrator.applicationConfig.bpdm.security.auth-server-url | string | `"http://centralidp.tx.test/auth"` |  |
| bpdm.bpdm-orchestrator.applicationConfig.bpdm.security.client-id | string | `"Cl25-CX-BPDM-Orchestrator"` |  |
| bpdm.bpdm-orchestrator.applicationConfig.bpdm.security.realm | string | `"CX-Central"` |  |
| bpdm.bpdm-orchestrator.applicationConfig.server.forward-headers-strategy | string | `"FRAMEWORK"` |  |
| bpdm.bpdm-orchestrator.applicationSecrets.spring.datasource.password | string | `"dbpasswordbpdm"` |  |
| bpdm.bpdm-orchestrator.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| bpdm.bpdm-orchestrator.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| bpdm.bpdm-orchestrator.ingress.annotations."nginx.ingress.kubernetes.io/x-forwarded-prefix" | string | `"/orchestrator"` |  |
| bpdm.bpdm-orchestrator.ingress.enabled | bool | `true` |  |
| bpdm.bpdm-orchestrator.ingress.hosts[0].host | string | `"business-partners.tx.test"` |  |
| bpdm.bpdm-orchestrator.ingress.hosts[0].paths[0].path | string | `"/orchestrator(/|$)(.*)"` |  |
| bpdm.bpdm-orchestrator.ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| bpdm.bpdm-orchestrator.postgres.enabled | bool | `false` |  |
| bpdm.bpdm-orchestrator.postgres.fullnameOverride | string | `"bpdm-postgres"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.client.orchestrator.base-url | string | `"http://business-partners.tx.test/orchestrator"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.client.orchestrator.registration.client-id | string | `"sa-cl25-cx-2"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.datasource.host | string | `"bpdm-postgres"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.security.auth-server-url | string | `"http://centralidp.tx.test/auth"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.security.client-id | string | `"Cl7-CX-BPDM"` |  |
| bpdm.bpdm-pool.applicationConfig.bpdm.security.realm | string | `"CX-Central"` |  |
| bpdm.bpdm-pool.applicationConfig.server.forward-headers-strategy | string | `"FRAMEWORK"` |  |
| bpdm.bpdm-pool.applicationSecrets.bpdm.client.orchestrator.registration.client-secret | string | `"changeme"` |  |
| bpdm.bpdm-pool.applicationSecrets.spring.datasource.password | string | `"dbpasswordbpdm"` |  |
| bpdm.bpdm-pool.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| bpdm.bpdm-pool.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| bpdm.bpdm-pool.ingress.annotations."nginx.ingress.kubernetes.io/x-forwarded-prefix" | string | `"/pool"` |  |
| bpdm.bpdm-pool.ingress.enabled | bool | `true` |  |
| bpdm.bpdm-pool.ingress.hosts[0].host | string | `"business-partners.tx.test"` |  |
| bpdm.bpdm-pool.ingress.hosts[0].paths[0].path | string | `"/pool(/|$)(.*)"` |  |
| bpdm.bpdm-pool.ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| bpdm.bpdm-pool.postgres.fullnameOverride | string | `nil` |  |
| bpdm.bpdm-pool.postgres.nameOverride | string | `"bpdm-postgres"` |  |
| bpdm.centralidp.enabled | bool | `false` |  |
| bpdm.enabled | bool | `false` |  |
| bpdm.postgres.architecture | string | `"standalone"` |  |
| bpdm.postgres.auth.password | string | `"dbpasswordbpdm"` |  |
| bpdm.postgres.auth.postgresPassword | string | `"dbpasswordbpdm"` |  |
| bpdm.postgres.fullnameOverride | string | `"bpdm-postgres"` |  |
| bpdm.postgres.image.repository | string | `"bitnamilegacy/postgresql"` |  |
| bpdm.postgres.image.tag | string | `"15-debian-11"` |  |
| bpdm.postgres.nameOverride | string | `nil` |  |
| bpdm.postgres.primary.persistence.enabled | bool | `false` |  |
| bpndiscovery.bpndiscovery.authentication | bool | `true` |  |
| bpndiscovery.bpndiscovery.bpndiscoveryEndpoint.allowedTypes | string | `"oen,wmi,passtype,manufacturerPartId"` |  |
| bpndiscovery.bpndiscovery.bpndiscoveryEndpoint.description | string | `"Service to discover BPN for different kind of type numbers"` |  |
| bpndiscovery.bpndiscovery.bpndiscoveryEndpoint.documentation | string | `"/bpndiscovery/swagger-ui/index.html"` |  |
| bpndiscovery.bpndiscovery.bpndiscoveryEndpoint.endpointAddress | string | `"/bpndiscovery"` |  |
| bpndiscovery.bpndiscovery.bpndiscoveryEndpoint.timeToLive | string | `"31536000"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.baseUrl | string | `"semantics.tx.test/discoveryfinder"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.provider.tokenUri | string | `"http://centralidp.tx.test/auth/realms/CX-Central/protocol/openid-connect/token"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.registration.authorizationGrantType | string | `"client_credentials"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.registration.clientId | string | `"sa-cl21-01"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.registration.clientSecret | string | `"changeme"` |  |
| bpndiscovery.bpndiscovery.discoveryfinderClient.schedulerCronFrequency | string | `"0 0 */1 * * *"` |  |
| bpndiscovery.bpndiscovery.host | string | `"semantics.tx.test"` |  |
| bpndiscovery.bpndiscovery.idp.issuerUri | string | `"http://centralidp.tx.test/auth/realms/CX-Central"` |  |
| bpndiscovery.bpndiscovery.idp.publicClientId | string | `"Cl22-CX-BPND"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."cert-manager.io/cluster-issuer" | string | `"my-ca-issuer"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-credentials" | string | `"true"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| bpndiscovery.bpndiscovery.ingress.annotations."nginx.ingress.kubernetes.io/x-forwarded-prefix" | string | `"/bpndiscovery"` |  |
| bpndiscovery.bpndiscovery.ingress.className | string | `"nginx"` |  |
| bpndiscovery.bpndiscovery.ingress.enabled | bool | `true` |  |
| bpndiscovery.bpndiscovery.ingress.tls | bool | `false` |  |
| bpndiscovery.bpndiscovery.ingress.urlPrefix | string | `"/bpndiscovery"` |  |
| bpndiscovery.bpndiscovery.livenessProbe.initialDelaySeconds | int | `200` |  |
| bpndiscovery.bpndiscovery.readinessProbe.initialDelaySeconds | int | `200` |  |
| bpndiscovery.enablePostgres | bool | `true` |  |
| bpndiscovery.enabled | bool | `false` |  |
| bpndiscovery.postgresql.auth.password | string | `"dbpasswordbpndiscovery"` |  |
| bpndiscovery.postgresql.auth.postgresPassword | string | `"dbpasswordbpndiscovery"` |  |
| bpndiscovery.postgresql.image.registry | string | `"docker.io"` |  |
| bpndiscovery.postgresql.image.repository | string | `"bitnamilegacy/postgresql"` |  |
| bpndiscovery.postgresql.image.tag | string | `"15-debian-11"` |  |
| bpndiscovery.postgresql.nameOverride | string | `"bpndiscovery-postgresql"` |  |
| bpndiscovery.postgresql.primary.persistence.enabled | bool | `false` |  |
| bpndiscovery.postgresql.primary.persistence.size | string | `"8Gi"` |  |
| centralidp.enabled | bool | `false` |  |
| centralidp.keycloak.auth.adminPassword | string | `"adminconsolepwcentralidp"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-credentials" | string | `"true"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-methods" | string | `"PUT, GET, POST, OPTIONS"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-origin" | string | `"http://centralidp.tx.test"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffer-size" | string | `"128k"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffering" | string | `"on"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffers-number" | string | `"20"` |  |
| centralidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| centralidp.keycloak.ingress.enabled | bool | `true` |  |
| centralidp.keycloak.ingress.hostname | string | `"centralidp.tx.test"` |  |
| centralidp.keycloak.ingress.ingressClassName | string | `"nginx"` |  |
| centralidp.keycloak.ingress.tls | bool | `false` |  |
| centralidp.keycloak.nameOverride | string | `"centralidp"` |  |
| centralidp.keycloak.postgresql.architecture | string | `"standalone"` |  |
| centralidp.keycloak.postgresql.auth.password | string | `"dbpasswordcentralidp"` |  |
| centralidp.keycloak.postgresql.auth.postgresPassword | string | `"dbpasswordcentralidp"` |  |
| centralidp.keycloak.postgresql.nameOverride | string | `"centralidp-postgresql"` |  |
| centralidp.keycloak.postgresql.primary.persistence.enabled | bool | `false` |  |
| centralidp.keycloak.replicaCount | int | `1` |  |
| centralidp.realmSeeding.bpn | string | `"BPNL00000003CRHK"` |  |
| centralidp.realmSeeding.clients.bpdm.clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.clients.bpdm.redirects[0] | string | `"http://partners-pool.tx.test/*"` |  |
| centralidp.realmSeeding.clients.bpdmGate.clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.clients.bpdmGate.redirects[0] | string | `"http://partners-gate.tx.test/*"` |  |
| centralidp.realmSeeding.clients.bpdmOrchestrator.clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.clients.miw.clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.clients.miw.redirects[0] | string | `"http://managed-identity-wallets.tx.test/*"` |  |
| centralidp.realmSeeding.clients.portal.redirects[0] | string | `"http://portal.tx.test/*"` |  |
| centralidp.realmSeeding.clients.portal.rootUrl | string | `"http://portal.tx.test/home"` |  |
| centralidp.realmSeeding.clients.registration.redirects[0] | string | `"http://portal.tx.test/*"` |  |
| centralidp.realmSeeding.clients.semantics.redirects[0] | string | `"http://portal.tx.test/*"` |  |
| centralidp.realmSeeding.extraServiceAccounts | object | `{"clientSecretsAndBpn":[{"bpn":"BPNL00000003AZQP","clientId":"satest01","clientSecret":"UbfW4CR1xH4OskkovqJ2JzcwnQIrG7oj"},{"bpn":"BPNL00000003AYRE","clientId":"satest02","clientSecret":"pyFUZP2L9UCSVJUScHcN3ZEgy2PGyEpg"},{"bpn":"BPNL00000003AVTH","clientId":"satest03","clientSecret":"tPwy4exxH1sXBRQouobSA2nNVaaPuwCs"},{"bpn":"BPNL00000003AWSS","clientId":"satest04","clientSecret":"BxZ3cwYUPJKK7gI4wq7q6Hgoxel6MphF"},{"bpn":"BPNL00000003B0Q0","clientId":"satest05","clientSecret":"dR00GN1AWCYbRGbZY8TXjs2YEPMeCxLF"},{"bpn":"BPNS0000000008ZZ","clientId":"satest06","clientSecret":"pDSziT0TUFAkMx0qGFcvpE4XkMqPh13v"},{"bpn":"BPNL00000003CNKC","clientId":"satest07","clientSecret":"GY5a44sNuNIjrTyjHvdEPLeNRHH0Kt39"},{"bpn":"BPNL00000003B6LU","clientId":"satest08","clientSecret":"WUXpQx1aIclA7enqtk4o2uvLDLMreUMI"},{"bpn":"BPNL00000003CML1","clientId":"satest09","clientSecret":"N08TGNdhUskJcmVEnOh1tAGwr9oca9PU"},{"bpn":"BPNS00000008BDFH","clientId":"satest10","clientSecret":"gzdSG0CBDJrtv1gje0zUASu1S9P4I7xP"},{"bpn":"BPNL00000003B2OM","clientId":"satest11","clientSecret":"CC3fz3dQGZsBp2NCbowOV65efBFZTgEO"},{"bpn":"BPNL00000003CSGV","clientId":"satest12","clientSecret":"2gjSlFxBO7spEM4aTz3f8CqDS0klbt7C"},{"bpn":"BPNL00000003B5MJ","clientId":"satest13","clientSecret":"3YQzDqEsdUZ83DVHSIRYUCK4pot61r5M"},{"bpn":"BPNL00000003AXS3","clientId":"satest14","clientSecret":"7qtMpfN3otq5dGiEPssVongXK56lb9LE"},{"bpn":"BPNL00000003B3NX","clientId":"satest15","clientSecret":"8QiZ8ineW0Lt8ZOlC2MYuCR0TvM6vMYX"},{"bpn":"BPNL00000000BJTL","clientId":"satest16","clientSecret":"d2sqUurBH9Vd8DNRmjiMfObU67ajorCq"}]}` | test service accounts for EDC - MIW which are obsolete since R24.05; uncomment once EDC uses SSI DIM Wallet Stub and the helm chart testing has been updated; currently the post-install testdata-upload-job fails if not available |
| centralidp.realmSeeding.initContainer.image.name | string | `"docker.io/tractusx/umbrella-init-container:2.3.0-init"` |  |
| centralidp.realmSeeding.initContainer.image.pullPolicy | string | `"IfNotPresent"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[0].clientId | string | `"sa-cl1-reg-2"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[0].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[10].clientId | string | `"sa-cl7-cx-5"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[10].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[11].clientId | string | `"sa-cl7-cx-7"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[11].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[12].clientId | string | `"sa-cl8-cx-1"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[12].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[13].clientId | string | `"sa-cl21-01"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[13].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[14].clientId | string | `"sa-cl22-01"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[14].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[15].clientId | string | `"sa-cl24-01"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[15].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[16].clientId | string | `"sa-cl25-cx-1"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[16].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[17].clientId | string | `"sa-cl25-cx-2"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[17].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[18].clientId | string | `"sa-cl25-cx-3"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[18].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[1].clientId | string | `"sa-cl2-01"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[1].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[2].clientId | string | `"sa-cl2-02"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[2].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[3].clientId | string | `"sa-cl2-03"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[3].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[4].clientId | string | `"sa-cl2-04"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[4].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[5].clientId | string | `"sa-cl2-05"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[5].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[6].clientId | string | `"sa-cl2-06"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[6].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[7].clientId | string | `"sa-cl3-cx-1"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[7].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[8].clientId | string | `"sa-cl5-custodian-2"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[8].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[9].clientId | string | `"sa-cl7-cx-1"` |  |
| centralidp.realmSeeding.serviceAccounts.clientSecrets[9].clientSecret | string | `"changeme"` |  |
| centralidp.realmSeeding.sharedidp | string | `"http://sharedidp.tx.test"` |  |
| centralidp.realmSeeding.sslRequired | string | `"none"` |  |
| cert-manager.enabled | bool | `false` |  |
| dataconsumerOne.data-persistence-layer-bundle.enabled | bool | `false` |  |
| dataconsumerOne.dataspace-connector-bundle.postgresql.auth.password | string | `"dbpassworddataconsumerone"` |  |
| dataconsumerOne.dataspace-connector-bundle.postgresql.auth.postgresPassword | string | `"dbpassworddataconsumerone"` |  |
| dataconsumerOne.dataspace-connector-bundle.postgresql.nameOverride | string | `"dataconsumer-1-db"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.bdrs.server.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/v1/directory"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.endpoints.management.authKey | string | `"TEST1"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].className | string | `"nginx"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].enabled | bool | `true` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[1] | string | `"protocol"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[2] | string | `"management"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].hostname | string | `"dataconsumer-1-controlplane.tx.test"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].tls.enabled | bool | `false` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].className | string | `"nginx"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].enabled | bool | `true` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[1] | string | `"public"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].hostname | string | `"dataconsumer-1-dataplane.tx.test"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].tls.enabled | bool | `false` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.token.signer.privatekey_alias | string | `"tokenSignerPrivateKey"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.dataplane.token.verifier.publickey_alias | string | `"tokenSignerPublicKey"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.id | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AZQP"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.sts.dim.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/sts"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.id | string | `"BPNL00000003AZQP"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.secret_alias | string | `"edc-wallet-secret"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.token_url | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.iatp.trustedIssuers[0] | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.nameOverride | string | `"dataconsumer-1-edc"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.participant.id | string | `"BPNL00000003AZQP"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.postgresql.auth.password | string | `"dbpassworddataconsumerone"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.postgresql.auth.postgresPassword | string | `"dbpassworddataconsumerone"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.postgresql.jdbcUrl | string | `"jdbc:postgresql://{{ .Release.Name }}-dataconsumer-1-db:5432/edc"` |  |
| dataconsumerOne.dataspace-connector-bundle.tractusx-connector.vault.hashicorp.url | string | `"http://{{ .Release.Name }}-edc-dataconsumer-1-vault:8200"` |  |
| dataconsumerOne.dataspace-connector-bundle.vault.enabled | bool | `true` |  |
| dataconsumerOne.dataspace-connector-bundle.vault.nameOverride | string | `"edc-dataconsumer-1-vault"` |  |
| dataconsumerOne.digital-twin-bundle.enabled | bool | `false` |  |
| dataconsumerOne.enabled | bool | `false` |  |
| dataconsumerOne.nameOverride | string | `"dataconsumer-1"` |  |
| dataconsumerOne.secrets.edc-wallet-secret | string | `"changeme"` |  |
| dataconsumerOne.seedTestdata | bool | `false` |  |
| dataconsumerTwo.data-persistence-layer-bundle.enabled | bool | `false` |  |
| dataconsumerTwo.dataspace-connector-bundle.postgresql.auth.password | string | `"dbpassworddataconsumertwo"` |  |
| dataconsumerTwo.dataspace-connector-bundle.postgresql.auth.postgresPassword | string | `"dbpassworddataconsumertwo"` |  |
| dataconsumerTwo.dataspace-connector-bundle.postgresql.nameOverride | string | `"dataconsumer-2-db"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.bdrs.server.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/v1/directory"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.endpoints.management.authKey | string | `"TEST3"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].className | string | `"nginx"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].enabled | bool | `true` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[1] | string | `"protocol"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[2] | string | `"management"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].hostname | string | `"dataconsumer-2-controlplane.tx.test"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].tls.enabled | bool | `false` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].className | string | `"nginx"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].enabled | bool | `true` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[1] | string | `"public"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].hostname | string | `"dataconsumer-2-dataplane.tx.test"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].tls.enabled | bool | `false` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.token.signer.privatekey_alias | string | `"tokenSignerPrivateKey"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.dataplane.token.verifier.publickey_alias | string | `"tokenSignerPublicKey"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.id | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AVTH"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.sts.dim.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/sts"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.id | string | `"BPNL00000003AVTH"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.secret_alias | string | `"edc-wallet-secret"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.token_url | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.iatp.trustedIssuers[0] | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.nameOverride | string | `"dataconsumer-2-edc"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.participant.id | string | `"BPNL00000003AVTH"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.postgresql.auth.password | string | `"dbpassworddataconsumertwo"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.postgresql.auth.postgresPassword | string | `"dbpassworddataconsumertwo"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.postgresql.jdbcUrl | string | `"jdbc:postgresql://{{ .Release.Name }}-dataconsumer-2-db:5432/edc"` |  |
| dataconsumerTwo.dataspace-connector-bundle.tractusx-connector.vault.hashicorp.url | string | `"http://{{ .Release.Name }}-edc-dataconsumer-2-vault:8200"` |  |
| dataconsumerTwo.dataspace-connector-bundle.vault.nameOverride | string | `"edc-dataconsumer-2-vault"` |  |
| dataconsumerTwo.digital-twin-bundle.enabled | bool | `false` |  |
| dataconsumerTwo.enabled | bool | `false` |  |
| dataconsumerTwo.nameOverride | string | `"dataconsumer-2"` |  |
| dataconsumerTwo.secrets.edc-wallet-secret | string | `"changeme"` |  |
| dataconsumerTwo.seedTestdata | bool | `false` |  |
| discoveryfinder.discoveryfinder.authentication | bool | `true` |  |
| discoveryfinder.discoveryfinder.dataSource.url | string | `"jdbc:postgresql://{{ .Release.Name }}-discoveryfinder-postgresql:5432/discoveryfinder"` |  |
| discoveryfinder.discoveryfinder.host | string | `"semantics.tx.test"` |  |
| discoveryfinder.discoveryfinder.idp.issuerUri | string | `"http://centralidp.tx.test/auth/realms/CX-Central"` |  |
| discoveryfinder.discoveryfinder.idp.publicClientId | string | `"Cl21-CX-DF"` |  |
| discoveryfinder.discoveryfinder.ingress | object | `{"annotations":{"cert-manager.io/cluster-issuer":"my-ca-issuer","nginx.ingress.kubernetes.io/cors-allow-credentials":"true","nginx.ingress.kubernetes.io/enable-cors":"true","nginx.ingress.kubernetes.io/rewrite-target":"/$2","nginx.ingress.kubernetes.io/use-regex":"true","nginx.ingress.kubernetes.io/x-forwarded-prefix":"/discoveryfinder"},"className":"nginx","enabled":true,"tls":false,"urlPrefix":"/discoveryfinder"}` | docs: http://semantics.tx.test/discoveryfinder/swagger-ui/index.html |
| discoveryfinder.discoveryfinder.livenessProbe.initialDelaySeconds | int | `200` |  |
| discoveryfinder.discoveryfinder.properties.discoveryfinder.initialEndpoints[0].description | string | `"Service to discover connector endpoints based on bpns"` |  |
| discoveryfinder.discoveryfinder.properties.discoveryfinder.initialEndpoints[0].documentation | string | `"http://portal-backend.tx.test/api/administration/swagger/index.html"` |  |
| discoveryfinder.discoveryfinder.properties.discoveryfinder.initialEndpoints[0].endpointAddress | string | `"http://portal-backend.tx.test/api/administration/Connectors/discovery"` |  |
| discoveryfinder.discoveryfinder.properties.discoveryfinder.initialEndpoints[0].type | string | `"bpn"` |  |
| discoveryfinder.discoveryfinder.readinessProbe.initialDelaySeconds | int | `200` |  |
| discoveryfinder.enablePostgres | bool | `true` |  |
| discoveryfinder.enabled | bool | `false` |  |
| discoveryfinder.postgresql.auth.password | string | `"dbpassworddiscoveryfinder"` |  |
| discoveryfinder.postgresql.auth.postgresPassword | string | `"dbpassworddiscoveryfinder"` |  |
| discoveryfinder.postgresql.image.registry | string | `"docker.io"` |  |
| discoveryfinder.postgresql.image.repository | string | `"bitnamilegacy/postgresql"` |  |
| discoveryfinder.postgresql.image.tag | string | `"15-debian-11"` |  |
| discoveryfinder.postgresql.nameOverride | string | `"discoveryfinder-postgresql"` |  |
| discoveryfinder.postgresql.primary.persistence.enabled | bool | `false` |  |
| discoveryfinder.postgresql.primary.persistence.size | string | `"8Gi"` |  |
| external-secrets.enabled | bool | `false` |  |
| grafana.enabled | bool | `false` |  |
| identity-and-trust-bundle.enabled | bool | `false` |  |
| identity-and-trust-bundle.postgresql.auth.password | string | `"postgrespassword"` |  |
| identity-and-trust-bundle.postgresql.auth.username | string | `"postgres"` |  |
| identity-and-trust-bundle.postgresql.configmap.name | string | `"wallet-postgres-configmap"` |  |
| identity-and-trust-bundle.postgresql.enabled | bool | `true` |  |
| identity-and-trust-bundle.postgresql.fullnameOverride | string | `"wallet-postgres"` |  |
| identity-and-trust-bundle.postgresql.persistence.enabled | bool | `false` |  |
| identity-and-trust-bundle.postgresql.persistence.size | string | `"10Gi"` |  |
| identity-and-trust-bundle.postgresql.persistence.storageClass | string | `"standard"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.appName | string | `"ssi-dim-wallet-stub"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.baseWalletBpn | string | `"BPNL00000003CRHK"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.configName | string | `"ssi-dim-wallet-config"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.didHost | string | `"ssi-dim-wallet-stub.tx.test"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.environment | string | `"default"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.host | string | `"ssi-dim-wallet-stub.tx.test"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.annotations | object | `{}` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.className | string | `"nginx"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.enabled | bool | `true` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.tls.enabled | bool | `false` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.tls.name | string | `""` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingress.urlPrefix | string | `"/"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.ingressName | string | `"ssi-dim-wallet-ingress"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.keycloak.authServerUrl | string | `"http://centralidp.tx.test/auth"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.keycloak.realm | string | `"CX-Central"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.logLevel | string | `"debug"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.nameSpace | string | `"umbrella"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.portal.clientId | string | `"sa-cl2-05"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.portal.clientSecret | string | `"changeme"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.portal.host | string | `"http://portal-backend.tx.test"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.portal.waitTime | string | `"60"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.postgresql.password | string | `"postgrespassword"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.postgresql.username | string | `"postgres"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.replicaCount | int | `1` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.resources.limits.cpu | int | `1` | CPU resource limits |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.resources.limits.memory | string | `"2Gi"` | Memory resource limits |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.resources.requests.cpu | string | `"500m"` | CPU resource requests |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.resources.requests.memory | string | `"1Gi"` | Memory resource requests |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.secretName | string | `"ssi-dim-wallet-secret"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.seeding.bpnList | string | `"BPNL00000003AZQP,BPNL00000003AYRE"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.service.port | int | `8080` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.service.type | string | `"ClusterIP"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.serviceName | string | `"ssi-dim-wallet-service"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.statusListVcId | string | `"8a6c7486-1e1f-4555-bdd2-1a178182651e"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.stubUrl | string | `"http://ssi-dim-wallet-stub.tx.test"` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.swagger.apiDoc.status | bool | `true` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.swagger.ui.status | bool | `true` |  |
| identity-and-trust-bundle.ssi-dim-wallet-stub.wallet.tokenExpiryTime | string | `"5"` |  |
| jaeger.enabled | bool | `false` |  |
| loki.enabled | bool | `false` |  |
| opentelemetry-collector.enabled | bool | `false` |  |
| pgadmin4.enabled | bool | `false` |  |
| pgadmin4.env.email | string | `"pgadmin4@txtest.org"` |  |
| pgadmin4.env.password | string | `"tractusxpgadmin4"` |  |
| pgadmin4.ingress.enabled | bool | `true` |  |
| pgadmin4.ingress.hosts[0].host | string | `"pgadmin4.tx.test"` |  |
| pgadmin4.ingress.hosts[0].paths[0].path | string | `"/"` |  |
| pgadmin4.ingress.hosts[0].paths[0].pathType | string | `"Prefix"` |  |
| pgadmin4.ingress.ingressClassName | string | `"nginx"` |  |
| pgadmin4.persistentVolume.enabled | bool | `false` |  |
| portal.backend.administration.issuerdid | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| portal.backend.administration.logging.bpdmLibrary | string | `"Debug"` |  |
| portal.backend.administration.logging.businessLogic | string | `"Debug"` |  |
| portal.backend.administration.logging.custodianLibrary | string | `"Debug"` |  |
| portal.backend.administration.logging.default | string | `"Debug"` |  |
| portal.backend.administration.logging.sdfactoryLibrary | string | `"Debug"` |  |
| portal.backend.administration.serviceAccount.encryptionConfigs.index0.encryptionKey | string | `"deb8261ec7b89c344f1c5ef5a11606e305f14e0d231b1357d90ad0180c5081d3"` |  |
| portal.backend.administration.swaggerEnabled | bool | `true` |  |
| portal.backend.appmarketplace.logging.default | string | `"Debug"` |  |
| portal.backend.appmarketplace.logging.offersLibrary | string | `"Debug"` |  |
| portal.backend.appmarketplace.swaggerEnabled | bool | `true` |  |
| portal.backend.dotnetEnvironment | string | `"Development"` |  |
| portal.backend.ingress | object | `{"annotations":{"nginx.ingress.kubernetes.io/cors-allow-origin":"http://localhost:3000, http://*.tx.test","nginx.ingress.kubernetes.io/enable-cors":"true","nginx.ingress.kubernetes.io/proxy-body-size":"8m","nginx.ingress.kubernetes.io/use-regex":"true"},"className":"nginx","enabled":true,"hosts":[{"host":"portal-backend.tx.test","paths":[{"backend":{"port":8080,"service":"registration-service"},"path":"/api/registration","pathType":"Prefix"},{"backend":{"port":8080,"service":"administration-service"},"path":"/api/administration","pathType":"Prefix"},{"backend":{"port":8080,"service":"notification-service"},"path":"/api/notification","pathType":"Prefix"},{"backend":{"port":8080,"service":"provisioning-service"},"path":"/api/provisioning","pathType":"Prefix"},{"backend":{"port":8080,"service":"marketplace-app-service"},"path":"/api/apps","pathType":"Prefix"},{"backend":{"port":8080,"service":"services-service"},"path":"/api/services","pathType":"Prefix"}]}],"name":"portal-backend"}` | docs: http://portal-backend.tx.test/api/administration/swagger/index.html http://portal-backend.tx.test/api/registration/swagger/index.html http://portal-backend.tx.test/api/apps/swagger/index.html http://portal-backend.tx.test/api/services/swagger/index.html http://portal-backend.tx.test/api/notification/swagger/index.html |
| portal.backend.keycloak.central.clientId | string | `"sa-cl1-reg-2"` |  |
| portal.backend.keycloak.central.clientSecret | string | `"changeme"` |  |
| portal.backend.keycloak.central.jwtBearerOptions.requireHttpsMetadata | string | `"false"` |  |
| portal.backend.keycloak.shared.clientId | string | `"sa-cl1-reg-1"` |  |
| portal.backend.keycloak.shared.clientSecret | string | `"changeme"` |  |
| portal.backend.mailing.host | string | `"smtp.tx.test"` |  |
| portal.backend.mailing.password | string | `""` |  |
| portal.backend.mailing.port | string | `"587"` |  |
| portal.backend.mailing.senderEmail | string | `"smtp@tx.test"` |  |
| portal.backend.mailing.user | string | `"smtp-user"` |  |
| portal.backend.notification.logging.default | string | `"Debug"` |  |
| portal.backend.notification.swaggerEnabled | bool | `true` |  |
| portal.backend.portalmigrations.logging.default | string | `"Debug"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.enabled | bool | `true` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company10.bpn | string | `"BPNS00000008BDFH"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company10.connectorName | string | `"BPN TRACEX B SITE A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company10.connectorUrl | string | `"http://company10-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company10.name | string | `"BPN_TRACEX_B_SITE_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company11.bpn | string | `"BPNL00000003B2OM"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company11.connectorName | string | `"BPN TIER A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company11.connectorUrl | string | `"http://company11-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company11.name | string | `"BPN_TIER_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company12.bpn | string | `"BPNL00000003CSGV"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company12.connectorName | string | `"BPN TIER C Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company12.connectorUrl | string | `"http://company12-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company12.name | string | `"BPN_TIER_C"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company13.bpn | string | `"BPNL00000003B5MJ"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company13.connectorName | string | `"BPN TIER B Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company13.connectorUrl | string | `"http://company13-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company13.name | string | `"BPN_TIER_B"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company14.bpn | string | `"BPNL00000003AXS3"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company14.connectorName | string | `"BPN SUB TIER B Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company14.connectorUrl | string | `"http://company14-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company14.name | string | `"BPN_SUB_TIER_B"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company15.bpn | string | `"BPNL00000003B3NX"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company15.connectorName | string | `"BPN SUB TIER A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company15.connectorUrl | string | `"http://company15-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company15.name | string | `"BPN_SUB_TIER_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company16.bpn | string | `"BPNL00000000BJTL"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company16.connectorName | string | `"BPN SUB TIER C Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company16.connectorUrl | string | `"http://company16-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company16.name | string | `"BPN_SUB_TIER_C"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company4.bpn | string | `"BPNL00000003AWSS"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company4.connectorName | string | `"BPN IRS TEST Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company4.connectorUrl | string | `"http://company4-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company4.name | string | `"BPN_IRS_TEST"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company5.bpn | string | `"BPNL00000003B0Q0"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company5.connectorName | string | `"BPN N TIER A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company5.connectorUrl | string | `"http://company5-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company5.name | string | `"BPN_N_TIER_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company6.bpn | string | `"BPNS0000000008ZZ"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company6.connectorName | string | `"BPN TRACEX A SITE A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company6.connectorUrl | string | `"http://company6-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company6.name | string | `"BPN_TRACEX_A_SITE_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company7.bpn | string | `"BPNL00000003CNKC"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company7.connectorName | string | `"BPN TRACEX B Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company7.connectorUrl | string | `"http://company7-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company7.name | string | `"BPN_TRACEX_B"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company8.bpn | string | `"BPNL00000003B6LU"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company8.connectorName | string | `"BPN DISMANTLER Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company8.connectorUrl | string | `"http://company8-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company8.name | string | `"BPN_DISMANTLER"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company9.bpn | string | `"BPNL00000003CML1"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company9.connectorName | string | `"BPN TRACEX A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company9.connectorUrl | string | `"http://company9-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.company9.name | string | `"BPN_TRACEX_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerOne.connectorName | string | `"BPN OEM C Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerOne.connectorUrl | string | `"http://dataconsumer-1-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerOne.name | string | `"BPN_OEM_C"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerTwo.connectorName | string | `"BPN OEM B Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerTwo.connectorUrl | string | `"http://dataconsumer-2-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.dataconsumerTwo.name | string | `"BPN_OEM_B"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.tx-data-provider.connectorName | string | `"BPN OEM A Connector"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.tx-data-provider.connectorUrl | string | `"http://dataprovider-controlplane.tx.test/api/v1/dsp"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.companies.tx-data-provider.name | string | `"BPN_OEM_A"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.configMap | string | `"portal-testdata"` |  |
| portal.backend.portalmigrations.seeding.seedTestData.useOwnConfigMap.filename | string | `"test"` |  |
| portal.backend.processesworker.bpdm.clientId | string | `"sa-cl7-cx-5"` |  |
| portal.backend.processesworker.bpdm.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.bpnDidResolver.apiKey | string | `""` | ApiKey for management endpoint of the bpnDidResolver. Secret-key 'bpndidresolver-api-key'. |
| portal.backend.processesworker.clearinghouseConnectDisabled | bool | `true` |  |
| portal.backend.processesworker.custodian.clientId | string | `"sa-cl5-custodian-2"` |  |
| portal.backend.processesworker.custodian.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.dim.baseAddress | string | `"http://ssi-dim-wallet-stub.tx.test"` |  |
| portal.backend.processesworker.dim.clientId | string | `"sa-cl2-05"` |  |
| portal.backend.processesworker.dim.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.dim.encryptionConfigs.index0.encryptionKey | string | `"6cbaf47ee30c778088e6faa44e2f0eed98beda86db06c7d2e37e32ab78e14b33"` |  |
| portal.backend.processesworker.dim.grantType | string | `"client_credentials"` |  |
| portal.backend.processesworker.dim.scope | string | `"openid"` |  |
| portal.backend.processesworker.dim.universalResolverAddress | string | `"https://dev.uniresolver.io/"` |  |
| portal.backend.processesworker.invitation.encryptionConfigs.index0.encryptionKey | string | `"d84fea29d6eac0fa51e36682b164e7d61693cd4202ed04306d2d9c5d46655e2c"` |  |
| portal.backend.processesworker.issuerComponent.clientId | string | `"sa-cl2-04"` |  |
| portal.backend.processesworker.issuerComponent.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.issuerComponent.encryptionConfigs.index0.encryptionKey | string | `"39ffab76f99ece1e4ac72f973d5c703737324a75c6445e84fa317a7833476a15"` |  |
| portal.backend.processesworker.logging.bpdmLibrary | string | `"Debug"` |  |
| portal.backend.processesworker.logging.clearinghouseLibrary | string | `"Debug"` |  |
| portal.backend.processesworker.logging.custodianLibrary | string | `"Debug"` |  |
| portal.backend.processesworker.logging.default | string | `"Debug"` |  |
| portal.backend.processesworker.logging.offerProvider | string | `"Debug"` |  |
| portal.backend.processesworker.logging.processesLibrary | string | `"Debug"` |  |
| portal.backend.processesworker.logging.sdfactoryLibrary | string | `"Debug"` |  |
| portal.backend.processesworker.mailing.encryptionConfigs.index0.encryptionKey | string | `"d2e27d71b018cb36029184852f1baa3e26891be94718f77de4c7cc6c882fe317"` |  |
| portal.backend.processesworker.offerprovider.clientId | string | `"sa-cl2-03"` |  |
| portal.backend.processesworker.offerprovider.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.offerprovider.encryptionConfigs.index0.encryptionKey | string | `"95ee1429aa40c6bb6972520a9626b19c4306baf0efe3441c8cd41918ea198921"` |  |
| portal.backend.processesworker.onboardingServiceProvider.encryptionConfigs.index0.cipherMode | string | `"CBC"` |  |
| portal.backend.processesworker.onboardingServiceProvider.encryptionConfigs.index0.encryptionKey | string | `"f7bc3d99f1ace73e7a75b794affbbc26206ab29909821a102aaccb2e95e45f7c"` |  |
| portal.backend.processesworker.onboardingServiceProvider.encryptionConfigs.index0.paddingMode | string | `"PKCS7"` |  |
| portal.backend.processesworker.onboardingServiceProvider.encryptionConfigs.index1.encryptionKey | string | `"8027152fe7a869c88acc86981760acd70ff1d660c2bd129eece94edef933caf7"` |  |
| portal.backend.processesworker.sdfactory.clientId | string | `"sa-cl8-cx-1"` |  |
| portal.backend.processesworker.sdfactory.clientSecret | string | `"changeme"` |  |
| portal.backend.processesworker.sdfactory.issuerBpn | string | `"BPNL00000003CRHK"` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.from | string | `"smtp@tx.test"` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.host | string | `"smtp.tx.test"` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.password | string | `""` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.port | string | `"587"` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.replyTo | string | `"smtp@tx.test"` |  |
| portal.backend.provisioning.sharedRealm.smtpServer.user | string | `"smtp-user"` |  |
| portal.backend.registration.logging.bpdmLibrary | string | `"Debug"` |  |
| portal.backend.registration.logging.default | string | `"Debug"` |  |
| portal.backend.registration.logging.registrationService | string | `"Debug"` |  |
| portal.backend.registration.swaggerEnabled | bool | `true` |  |
| portal.backend.services.logging.default | string | `"Debug"` |  |
| portal.backend.services.logging.offersLibrary | string | `"Debug"` |  |
| portal.backend.services.swaggerEnabled | bool | `true` |  |
| portal.backend.useDimWallet | bool | `true` |  |
| portal.bpdm.poolAddress | string | `"http://business-partners.tx.test"` |  |
| portal.bpdm.poolApiPath | string | `"/pool/v6"` |  |
| portal.bpdm.portalGateAddress | string | `"http://business-partners.tx.test"` |  |
| portal.bpdm.portalGateApiPath | string | `"/gate/v6"` |  |
| portal.centralidp.address | string | `"http://centralidp.tx.test"` |  |
| portal.clearinghouse.default.baseAddress | string | `"http://validation.tx.test"` |  |
| portal.clearinghouse.default.clearinghouseConnectDisabled | bool | `true` |  |
| portal.clearinghouse.default.clientId | string | `"clearinghouse-client-id-default"` | clientId and clientSecret aren't in the centralidp Keycloak |
| portal.clearinghouse.default.clientSecret | string | `""` |  |
| portal.clearinghouse.default.tokenAddress | string | `"http://someiam.tx.test/realms/example/protocol/openid-connect/token"` |  |
| portal.clearinghouseConnectDisabled | bool | `true` | no configuration for clearinghouse because it's an external component |
| portal.custodianAddress | string | `"http://ssi-dim-wallet-stub.tx.test"` |  |
| portal.decentralIdentityManagementAuthAddress | string | `"http://ssi-dim-wallet-stub.tx.test/api/sts"` |  |
| portal.dimWrapper.apiPath | string | `"/api/dim"` |  |
| portal.dimWrapper.baseAddress | string | `"http://ssi-dim-wallet-stub.tx.test"` |  |
| portal.dimWrapper.tokenAddress | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` |  |
| portal.enabled | bool | `false` |  |
| portal.frontend.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-origin" | string | `"http://*.tx.test"` |  |
| portal.frontend.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| portal.frontend.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$1"` |  |
| portal.frontend.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| portal.frontend.ingress.className | string | `"nginx"` |  |
| portal.frontend.ingress.enabled | bool | `true` |  |
| portal.frontend.ingress.hosts[0].host | string | `"portal.tx.test"` |  |
| portal.frontend.ingress.hosts[0].paths[0].backend.port | int | `8080` |  |
| portal.frontend.ingress.hosts[0].paths[0].backend.service | string | `"portal"` |  |
| portal.frontend.ingress.hosts[0].paths[0].path | string | `"/(.*)"` |  |
| portal.frontend.ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| portal.frontend.ingress.hosts[0].paths[1].backend.port | int | `8080` |  |
| portal.frontend.ingress.hosts[0].paths[1].backend.service | string | `"registration"` |  |
| portal.frontend.ingress.hosts[0].paths[1].path | string | `"/registration/(.*)"` |  |
| portal.frontend.ingress.hosts[0].paths[1].pathType | string | `"ImplementationSpecific"` |  |
| portal.frontend.ingress.hosts[0].paths[2].backend.port | int | `8080` |  |
| portal.frontend.ingress.hosts[0].paths[2].backend.service | string | `"assets"` |  |
| portal.frontend.ingress.hosts[0].paths[2].path | string | `"/((assets|documentation)/.*)"` |  |
| portal.frontend.ingress.hosts[0].paths[2].pathType | string | `"ImplementationSpecific"` |  |
| portal.issuerComponentAddress | string | `"http://ssi-credential-issuer.tx.test"` |  |
| portal.portalAddress | string | `"http://portal.tx.test"` |  |
| portal.portalBackendAddress | string | `"http://portal-backend.tx.test"` |  |
| portal.postgresql.architecture | string | `"standalone"` |  |
| portal.postgresql.auth.password | string | `"dbpasswordportal"` |  |
| portal.postgresql.auth.portalPassword | string | `"dbpasswordportal"` |  |
| portal.postgresql.auth.provisioningPassword | string | `"dbpasswordportal"` |  |
| portal.postgresql.auth.replicationPassword | string | `"dbpasswordportal"` |  |
| portal.postgresql.commonLabels."app.kubernetes.io/version" | string | `"15"` |  |
| portal.postgresql.enabled | bool | `true` |  |
| portal.postgresql.image.registry | string | `"docker.io"` |  |
| portal.postgresql.image.repository | string | `"bitnamilegacy/postgresql"` |  |
| portal.postgresql.image.tag | string | `"15-debian-11"` |  |
| portal.postgresql.nameOverride | string | `"portal-backend-postgresql"` |  |
| portal.postgresql.primary.persistence.enabled | bool | `false` |  |
| portal.replicaCount | int | `1` |  |
| portal.sdfactoryAddress | string | `"http://sdfactory.tx.test"` |  |
| portal.semanticsAddress | string | `"http://semantics.tx.test"` |  |
| portal.sharedidpAddress | string | `"http://sharedidp.tx.test"` |  |
| prometheus.enabled | bool | `false` |  |
| selfdescription.enabled | bool | `false` |  |
| selfdescription.ingress.className | string | `"nginx"` |  |
| selfdescription.ingress.enabled | bool | `true` |  |
| selfdescription.ingress.hosts[0].host | string | `"sdfactory.tx.test"` |  |
| selfdescription.ingress.hosts[0].paths[0].path | string | `"/"` |  |
| selfdescription.ingress.hosts[0].paths[0].pathType | string | `"Prefix"` |  |
| selfdescription.sdfactory.secret.clearingHouseClientId | string | `""` | Details for Clearing House Client ID |
| selfdescription.sdfactory.secret.clearingHouseClientSecret | string | `""` | Details for Clearing House Client Secret |
| selfdescription.sdfactory.secret.clearingHouseRealm | string | `""` | Details for Clearing House Realm |
| selfdescription.sdfactory.secret.clearingHouseServerUrl | string | `""` | Details for Clearing House URL |
| selfdescription.sdfactory.secret.clearingHouseUri | string | `""` | Details for Clearing House URI |
| selfdescription.sdfactory.secret.jwkSetUri | string | `"http://centralidp.tx.test/auth/realms/CX-Central/protocol/openid-connect/certs"` | JWK Set URI |
| selfdescription.sdfactory.secret.verifycredentialsUri | string | `""` | Details for Verifying Client uri |
| semantic-hub.enableKeycloak | bool | `false` |  |
| semantic-hub.enabled | bool | `false` |  |
| semantic-hub.graphdb.enabled | bool | `true` |  |
| semantic-hub.graphdb.image | string | `"jena-fuseki-docker:5.0.0"` |  |
| semantic-hub.graphdb.imagePullPolicy | string | `"Never"` |  |
| semantic-hub.graphdb.storageClassName | string | `""` |  |
| semantic-hub.graphdb.storageSize | string | `"8Gi"` |  |
| semantic-hub.hub.authentication | bool | `true` |  |
| semantic-hub.hub.embeddedTripleStore | bool | `true` |  |
| semantic-hub.hub.host | string | `"semantics.tx.test"` |  |
| semantic-hub.hub.idpClientId | string | `"Cl3-CX-Semantic"` |  |
| semantic-hub.hub.idpIssuerUri | string | `"http://centralidp.tx.test/auth/realms/CX-Central"` |  |
| semantic-hub.hub.ingress.annotations."cert-manager.io/cluster-issuer" | string | `"my-ca-issuer"` |  |
| semantic-hub.hub.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-credentials" | string | `"true"` |  |
| semantic-hub.hub.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| semantic-hub.hub.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| semantic-hub.hub.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| semantic-hub.hub.ingress.annotations."nginx.ingress.kubernetes.io/x-forwarded-prefix" | string | `"/hub"` |  |
| semantic-hub.hub.ingress.className | string | `"nginx"` |  |
| semantic-hub.hub.ingress.enabled | bool | `true` |  |
| semantic-hub.hub.ingress.tls | bool | `false` |  |
| semantic-hub.hub.ingress.urlPrefix | string | `"/hub"` |  |
| semantic-hub.hub.livenessProbe.initialDelaySeconds | int | `200` |  |
| semantic-hub.hub.readinessProbe.initialDelaySeconds | int | `200` |  |
| semantic-hub.keycloak.postgresql.architecture | string | `"standalone"` |  |
| semantic-hub.keycloak.postgresql.primary.persistence.enabled | bool | `false` |  |
| sharedidp.enabled | bool | `false` |  |
| sharedidp.keycloak.auth.adminPassword | string | `"adminconsolepwsharedidp"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-credentials" | string | `"true"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-methods" | string | `"PUT, GET, POST, OPTIONS"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-origin" | string | `"http://sharedidp.tx.test"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffer-size" | string | `"128k"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffering" | string | `"on"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/proxy-buffers-number" | string | `"20"` |  |
| sharedidp.keycloak.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| sharedidp.keycloak.ingress.enabled | bool | `true` |  |
| sharedidp.keycloak.ingress.hostname | string | `"sharedidp.tx.test"` |  |
| sharedidp.keycloak.ingress.ingressClassName | string | `"nginx"` |  |
| sharedidp.keycloak.ingress.tls | bool | `false` |  |
| sharedidp.keycloak.nameOverride | string | `"sharedidp"` |  |
| sharedidp.keycloak.postgresql.architecture | string | `"standalone"` |  |
| sharedidp.keycloak.postgresql.auth.password | string | `"dbpasswordsharedidp"` |  |
| sharedidp.keycloak.postgresql.auth.postgresPassword | string | `"dbpasswordsharedidp"` |  |
| sharedidp.keycloak.postgresql.nameOverride | string | `"sharedidp-postgresql"` |  |
| sharedidp.keycloak.postgresql.primary.persistence.enabled | bool | `false` |  |
| sharedidp.realmSeeding.realms.cxOperator.centralidp | string | `"http://centralidp.tx.test"` |  |
| sharedidp.realmSeeding.realms.cxOperator.initialUser.password | string | `"tractusx-umbr3lla!"` |  |
| sharedidp.realmSeeding.realms.cxOperator.initialUser.username | string | `"cx-operator@tx.test"` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.from | string | `"smtp@tx.test"` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.host | string | `"smtp.tx.test"` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.password | string | `""` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.port | string | `"587"` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.replyTo | string | `"smtp@tx.test"` |  |
| sharedidp.realmSeeding.realms.cxOperator.mailing.username | string | `"smtp-user"` |  |
| sharedidp.realmSeeding.realms.cxOperator.sslRequired | string | `"none"` |  |
| sharedidp.realmSeeding.realms.master.serviceAccounts.provisioning.clientSecret | string | `"changeme"` |  |
| sharedidp.realmSeeding.realms.master.serviceAccounts.saCxOperator.clientSecret | string | `"changeme"` |  |
| smtp4dev.enabled | bool | `false` |  |
| smtp4dev.ingress.url | string | `"smtp.tx.test"` |  |
| smtp4dev.ports.http | int | `80` |  |
| smtp4dev.ports.smtp | int | `25` |  |
| ssi-credential-issuer.centralidp.address | string | `"http://centralidp.tx.test"` | Provide centralidp base address (CX IAM), without trailing '/auth'. |
| ssi-credential-issuer.centralidp.jwtBearerOptions.requireHttpsMetadata | string | `"false"` |  |
| ssi-credential-issuer.credentialExpiry.logging.default | string | `"Debug"` |  |
| ssi-credential-issuer.enabled | bool | `false` |  |
| ssi-credential-issuer.ingress.annotations."nginx.ingress.kubernetes.io/cors-allow-origin" | string | `"http://*.tx.test"` |  |
| ssi-credential-issuer.ingress.annotations."nginx.ingress.kubernetes.io/enable-cors" | string | `"true"` |  |
| ssi-credential-issuer.ingress.annotations."nginx.ingress.kubernetes.io/proxy-body-size" | string | `"8m"` |  |
| ssi-credential-issuer.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| ssi-credential-issuer.ingress.className | string | `"nginx"` |  |
| ssi-credential-issuer.ingress.enabled | bool | `true` |  |
| ssi-credential-issuer.ingress.hosts[0].host | string | `"ssi-credential-issuer.tx.test"` |  |
| ssi-credential-issuer.ingress.hosts[0].paths[0].backend.port | int | `8080` |  |
| ssi-credential-issuer.ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ssi-credential-issuer.ingress.hosts[0].paths[0].pathType | string | `"Prefix"` |  |
| ssi-credential-issuer.ingress.tls | list | `[]` | Ingress TLS configuration |
| ssi-credential-issuer.migrations.logging.default | string | `"Debug"` |  |
| ssi-credential-issuer.portalBackendAddress | string | `"http://portal-backend.tx.test"` |  |
| ssi-credential-issuer.postgresql.architecture | string | `"standalone"` |  |
| ssi-credential-issuer.postgresql.auth.password | string | `"dbpasswordissuer"` | Password for the non-root username 'issuer'. Secret-key 'password'. |
| ssi-credential-issuer.postgresql.auth.postgrespassword | string | `"dbpasswordissuer"` | Password for the root username 'postgres'. Secret-key 'postgres-password'. |
| ssi-credential-issuer.postgresql.enabled | bool | `true` |  |
| ssi-credential-issuer.postgresql.image.repository | string | `"bitnamilegacy/postgresql"` |  |
| ssi-credential-issuer.postgresql.image.tag | string | `"15-debian-11"` |  |
| ssi-credential-issuer.postgresql.nameOverride | string | `"issuer-postgresql"` |  |
| ssi-credential-issuer.postgresql.primary.persistence.enabled | bool | `false` |  |
| ssi-credential-issuer.processesworker.logging.default | string | `"Debug"` |  |
| ssi-credential-issuer.processesworker.portal.clientId | string | `"sa-cl24-01"` | Provide portal client-id from CX IAM centralidp. You must specify the technical user with the required roles for the interaction with the portal |
| ssi-credential-issuer.processesworker.portal.clientSecret | string | `"changeme"` | Client-secret for portal client-id. Secret-key 'portal-client-secret'. |
| ssi-credential-issuer.processesworker.wallet.clientId | string | `"wallet-client-id"` | Provide wallet client-id from CX IAM centralidp. You must specify the technical user with the required roles for the interaction with the managed-identity-wallet |
| ssi-credential-issuer.processesworker.wallet.clientSecret | string | `""` | Client-secret for wallet client-id. Secret-key 'wallet-client-secret'. |
| ssi-credential-issuer.replicaCount | int | `1` |  |
| ssi-credential-issuer.service.credential.encryptionConfigIndex | int | `0` |  |
| ssi-credential-issuer.service.credential.encryptionConfigs.index0.encryptionKey | string | `"deb8261ec7b89c344f1c5ef5a11606e305f14e0d231b1357d90ad0180c5081d3"` |  |
| ssi-credential-issuer.service.credential.issuerBpn | string | `"BPNL00000003CRHK"` |  |
| ssi-credential-issuer.service.credential.issuerDid | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| ssi-credential-issuer.service.credential.statusListUrl | string | `"http://ssi-dim-wallet-stub.tx.test/status-list/BPNL00000003CRHK/8a6c7486-1e1f-4555-bdd2-1a178182651e"` |  |
| ssi-credential-issuer.service.logging.businessLogic | string | `"Debug"` |  |
| ssi-credential-issuer.service.logging.default | string | `"Debug"` |  |
| ssi-credential-issuer.service.portal.clientId | string | `"sa-cl24-01"` | Provide portal client-id from CX IAM centralidp. You must specify the technical user with the required roles for the interaction with the portal |
| ssi-credential-issuer.service.portal.clientSecret | string | `"changeme"` | Client-secret for portal client-id. Secret-key 'portal-client-secret'. |
| ssi-credential-issuer.service.swaggerEnabled | bool | `true` |  |
| ssi-credential-issuer.walletAddress | string | `"http://ssi-dim-wallet-stub.tx.test"` |  |
| ssi-credential-issuer.walletTokenAddress | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` |  |
| tx-data-provider.backendUrl | string | `"http://{{ .Release.Name }}-dataprovider-submodelserver:8080"` |  |
| tx-data-provider.controlplaneManagementUrl | string | `"http://{{ .Release.Name }}-dataprovider-edc-controlplane:8081"` |  |
| tx-data-provider.controlplanePublicUrl | string | `"http://{{ .Release.Name }}-dataprovider-edc-controlplane:8084"` |  |
| tx-data-provider.data-persistence-layer-bundle.enabled | bool | `true` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.ingress.className | string | `"nginx"` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.ingress.enabled | bool | `true` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.ingress.hosts[0].host | string | `"dataprovider-submodelserver.tx.test"` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.ingress.hosts[0].paths[0].path | string | `"/"` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.ingress.hosts[0].paths[0].pathType | string | `"Prefix"` |  |
| tx-data-provider.data-persistence-layer-bundle.simple-data-backend.nameOverride | string | `"dataprovider-submodelserver"` |  |
| tx-data-provider.dataplaneUrl | string | `"http://{{ .Release.Name }}-dataprovider-edc-dataplane:8081"` |  |
| tx-data-provider.dataspace-connector-bundle.postgresql.auth.password | string | `"dbpasswordtxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.postgresql.auth.postgresPassword | string | `"dbpasswordtxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.postgresql.auth.user | string | `"dbusertxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.postgresql.nameOverride | string | `"dataprovider-db"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.bdrs.server.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/v1/directory"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.endpoints.management.authKey | string | `"TEST2"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].className | string | `"nginx"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].enabled | bool | `true` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[1] | string | `"protocol"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].endpoints[2] | string | `"management"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].hostname | string | `"dataprovider-controlplane.tx.test"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.controlplane.ingresses[0].tls.enabled | bool | `false` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.env.EDC_IAM_DID_WEB_USE_HTTPS | bool | `false` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.env.TX_IAM_IATP_CREDENTIALSERVICE_URL | string | `"http://ssi-dim-wallet-stub.tx.test/api"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].className | string | `"nginx"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].enabled | bool | `true` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[0] | string | `"default"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].endpoints[1] | string | `"public"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].hostname | string | `"dataprovider-dataplane.tx.test"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.ingresses[0].tls.enabled | bool | `false` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.token.signer.privatekey_alias | string | `"tokenSignerPrivateKey"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.dataplane.token.verifier.publickey_alias | string | `"tokenSignerPublicKey"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.id | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003AYRE"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.sts.dim.url | string | `"http://ssi-dim-wallet-stub.tx.test/api/sts"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.id | string | `"BPNL00000003AYRE"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.client.secret_alias | string | `"edc-wallet-secret"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.sts.oauth.token_url | string | `"http://ssi-dim-wallet-stub.tx.test/oauth/token"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.iatp.trustedIssuers[0] | string | `"did:web:ssi-dim-wallet-stub.tx.test:BPNL00000003CRHK"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.nameOverride | string | `"dataprovider-edc"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.participant.id | string | `"BPNL00000003AYRE"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.postgresql.auth.password | string | `"dbpasswordtxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.postgresql.auth.postgresPassword | string | `"dbpasswordtxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.postgresql.auth.user | string | `"dbusertxdataprovider"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.postgresql.jdbcUrl | string | `"jdbc:postgresql://{{ .Release.Name }}-dataprovider-db:5432/edc"` |  |
| tx-data-provider.dataspace-connector-bundle.tractusx-connector.vault.hashicorp.url | string | `"http://{{ .Release.Name }}-edc-dataprovider-vault:8200"` |  |
| tx-data-provider.dataspace-connector-bundle.vault.enabled | bool | `true` |  |
| tx-data-provider.dataspace-connector-bundle.vault.nameOverride | string | `"edc-dataprovider-vault"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.nameOverride | string | `"dataprovider-dtr"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.authentication | bool | `false` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.dataSource.url | string | `"jdbc:postgresql://dataprovider-digital-twin-db:5432/dtr"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.host | string | `"dataprovider-dtr.tx.test"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.annotations."cert-manager.io/cluster-issuer" | string | `"my-ca-issuer"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.className | string | `"nginx"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.rules[0].host | string | `"dataprovider-dtr.tx.test"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.rules[0].http.paths[0].path | string | `"/semantics/registry(/|$)(.*)"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.rules[0].http.paths[0].pathType | string | `"ImplementationSpecific"` |  |
| tx-data-provider.digital-twin-bundle.digital-twin-registry.registry.ingress.urlPrefix | string | `""` |  |
| tx-data-provider.digital-twin-bundle.enabled | bool | `true` |  |
| tx-data-provider.digital-twin-bundle.postgresql.fullnameOverride | string | `"dataprovider-digital-twin-db"` |  |
| tx-data-provider.enabled | bool | `false` |  |
| tx-data-provider.nameOverride | string | `"dataprovider"` |  |
| tx-data-provider.registryUrl | string | `"http://{{ .Release.Name }}-dataprovider-dtr:8080/api/v3"` |  |
| tx-data-provider.secrets.edc-wallet-secret | string | `"changeme"` |  |
| tx-data-provider.seedTestdata | bool | `true` |  |

----------------------------------------------

## **Quick Links**

- [Latest Release Notes](../../docs/user/common/note-r2405-onwards/R24.05.md)
- [Setup Instructions](../../docs/README.md#setup-network--installation)
- [Guides](../../docs/user/common/guides)

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>