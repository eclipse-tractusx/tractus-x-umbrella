# Overall Seed Data

## Addresses

### Base addresses

- portal base address - portalAddress: "<https://portal.example.org>"
- portal-backend base address - portalBackendAddress: "<https://portal-backend.example.org>"
- centralidp base address (CX IAM) - centralidpAddress: "<https://centralidp.example.org>"
- sharedidp address (CX IAM) - sharedidpAddress: "<https://sharedidp.example.org>"
- semantics base address - semanticsAddress: "<https://semantics.example.org>"
- bpdm partners pool base address - bpdmPartnersPoolAddress: "<https://business-partners.example.org>"
- bpdm portal gate base address - bpdmPortalGateAddress: "<https://business-partners.example.org>"
- custodian base address - custodianAddress: "<https://managed-identity-wallets.example.org>"
- sdfactory base address - sdfactoryAddress: "<https://sdfactory.example.org>"
- clearinghouse base address - clearinghouseAddress: "<https://validation.example.org>"
- clearinghouse token address - clearinghouseTokenAddress: "<https://keycloak.example.org/realms/example/protocol/openid-connect/token>"

### Token Address

- "<https://centralidp.example.org/auth/realms/CX-Central/protocol/openid-connect/token>"

## Companies and BPNs

- "BPN_OEM_C" : "BPNL00000003AZQP",
- "BPN_OEM_A" : "BPNL00000003AYRE",
- "BPN_OEM_B" : "BPNL00000003AVTH",
- "BPN_IRS_TEST" : "BPNL00000003AWSS",
- "BPN_N_TIER_A" : "BPNL00000003B0Q0",
- "BPN_TRACEX_A_SITE_A" : "BPNS0000000008ZZ",
- "BPN_TRACEX_B" : "BPNL00000003CNKC",
- "BPN_DISMANTLER" : "BPNL00000003B6LU",
- "BPN_TRACEX_A" : "BPNL00000003CML1",
- "BPN_TRACEX_B_SITE_A" : "BPNS00000008BDFH",
- "BPN_TIER_A" : "BPNL00000003B2OM",
- "BPN_TIER_C" : "BPNL00000003CSGV",
- "BPN_TIER_B" : "BPNL00000003B5MJ",
- "BPN_SUB_TIER_B" : "BPNL00000003AXS3",
- "BPN_SUB_TIER_A" : "BPNL00000003B3NX",
- "BPN_SUB_TIER_C" : "BPNL00000000BJTL",

## Keycloak (CentralIdP and SharedIdP) Seeding

### CentralIdP: service Accounts for EDC - MIW (test data)

- "BPN_OEM_C" : "BPNL00000003AZQP"
    - name: EDC-MIW BPN_OEM_C
    - client id: satest01
    - client secret: UbfW4CR1xH4OskkovqJ2JzcwnQIrG7oj
- "BPN_OEM_A" : "BPNL00000003AYRE"
    - name: EDC-MIW BPN_OEM_A
    - client id: satest02
    - client secret: pyFUZP2L9UCSVJUScHcN3ZEgy2PGyEpg
- "BPN_OEM_B" : "BPNL00000003AVTH"
    - name: EDC-MIW BPN_OEM_B
    - client id: satest03
    - client secret: tPwy4exxH1sXBRQouobSA2nNVaaPuwCs
- "BPN_IRS_TEST" : "BPNL00000003AWSS"
    - name: EDC-MIW BPN_IRS_TEST
    - client id: satest04
    - client secret: BxZ3cwYUPJKK7gI4wq7q6Hgoxel6MphF
- "BPN_N_TIER_A" : "BPNL00000003B0Q0"
    - name: EDC-MIW BPN_N_TIER_A
    - client id: satest05
    - client secret: dR00GN1AWCYbRGbZY8TXjs2YEPMeCxLF
- "BPN_TRACEX_A_SITE_A" : "BPNS0000000008ZZ"
    - name: EDC-MIW BPN_TRACEX_A_SITE_A
    - client id: satest06
    - client secret: pDSziT0TUFAkMx0qGFcvpE4XkMqPh13v
- "BPN_TRACEX_B" : "BPNL00000003CNKC"
    - name: EDC-MIW BPN_TRACEX_B
    - client id: satest07
    - client secret: GY5a44sNuNIjrTyjHvdEPLeNRHH0Kt39
- "BPN_DISMANTLER" : "BPNL00000003B6LU"
    - name: EDC-MIW BPN_DISMANTLER
    - client id: satest08
    - client secret: WUXpQx1aIclA7enqtk4o2uvLDLMreUMI
- "BPN_TRACEX_A" : "BPNL00000003CML1"
    - name: EDC-MIW BPN_TRACEX_A
    - client id: satest09
    - client secret: N08TGNdhUskJcmVEnOh1tAGwr9oca9PU
- "BPN_TRACEX_B_SITE_A" : "BPNS00000008BDFH"
    - name: EDC-MIW BPN_TRACEX_B_SITE_A
    - client id: satest10
    - client secret: gzdSG0CBDJrtv1gje0zUASu1S9P4I7xP
- "BPN_TIER_A" : "BPNL00000003B2OM"
    - name: EDC-MIW BPN_TIER_A
    - client id: satest11
    - client secret: CC3fz3dQGZsBp2NCbowOV65efBFZTgEO
- "BPN_TIER_C" : "BPNL00000003CSGV"
    - name: EDC-MIW BPN_TIER_C
    - client id: satest12
    - client secret: 2gjSlFxBO7spEM4aTz3f8CqDS0klbt7C
- "BPN_TIER_B" : "BPNL00000003B5MJ"
    - name: EDC-MIW BPN_TIER_B
    - client id: satest13
    - client secret: 3YQzDqEsdUZ83DVHSIRYUCK4pot61r5M
- "BPN_SUB_TIER_B" : "BPNL00000003AXS3"
    - name: EDC-MIW BPN_SUB_TIER_B
    - client id: satest14
    - client secret: 7qtMpfN3otq5dGiEPssVongXK56lb9LE
- "BPN_SUB_TIER_A" : "BPNL00000003B3NX"
    - name: EDC-MIW BPN_SUB_TIER_A
    - client id: satest15
    - client secret: 8QiZ8ineW0Lt8ZOlC2MYuCR0TvM6vMYX
- "BPN_SUB_TIER_C" : "BPNL00000000BJTL"
    - name: EDC-MIW BPN_SUB_TIER_C
    - client id: satest16
    - client secret: d2sqUurBH9Vd8DNRmjiMfObU67ajorCq

### Fixed client secrets in base seeding

#### CentralIdP

- Confidential client for BPDM
    - client id: Cl7-CX-BPDM
    - client secret: 4pJIiaUsLeQsSH6OEqoZmq6aEsZkeBj2
- Confidential client for BPDM Portal Gate
    - client id: Cl16-CX-BPDMGate
    - client secret: q0ma25iV6bfqV6ho3kyWKnR1trp0IRez
- Confidential client for Managed Identity Wallet
    - client id: Cl5-CX-Custodian
    - client secret: XzZNs56cadY8b2P253By8GS4jbY7QCui
- Service account for Portal-Backend to call Keycloak (portal helm chart: backend.keycloak.central.clientId)
    - client id: sa-cl1-reg-2
    - client secret: aEoUADDw2aNPa0WAaKGAyKfC80n8sKxJ
- Service account Clearinghouse update application
    - client id: sa-cl2-01
    - client secret: w6Ib6d7hdltXwkdtsJYF3Cb6fEywia7S
- Service account SelfDescription (SD) update application
    - client id: sa-cl2-02
    - client secret: T1oUdErz8w7VbIbpAHDnTLeyssZ8wTmj
- Service account AutoSetup trigger - Portal to Vendor Autosetup (portal helm chart: backend.processesworker.offerprovider.clientId)
    - client id: sa-cl2-03
    - client secret: wyNYzSnyu4iGvj17XgLSl0aQxAPjTjmI
- Service account Discovery Finder
    - client id: sa-cl21-01
    - client secret: oFbXttMA7vI5MysN7AiEpobX5o3Jfbhp
- Service account BPN Discovery
    - client id: sa-cl22-01
    - client secret: 1yDWW7BNwouRGxYRkDmzkpzqz5FG748f
- Service account internal - communication GitHub and Semantic Hub
    - client id: sa-cl3-cx-1
    - client secret: jzTX8jBBpDCag224ihfhmBP5NABGqdsf
- Service account for SD Hub Call to Custodian for SD signature
    - client id: sa-cl5-custodian-1
    - client secret: 6pnnap7byS1TImL9Uj7g2psud9Fdq4tJ
- Service account for Portal to call Custodian Wallet (portal helm chart: backend.processesworker.custodian.clientId)
    - client id: sa-cl5-custodian-2
    - client secret: UIqawwoohsvZ6AZOd1llLhnsUTKMWe4D
- Service account for Portal to access BPDM for Company Address publishing into the BPDM (portal helm chart: backend.processesworker.bpdm.clientId)
    - client id: sa-cl7-cx-5
    - client secret: bWSck103qNJ0jZ1LVtG9mUAlcL7R5RLg
- Service account for Portal to SD (portal helm chart: backend.processesworker.sdfactory.clientId)
    - client id: sa-cl8-cx-1
    - client secret: clbQOPHcVKY9tUUd068vyf8CrsPZ8BgZ

#### SharedIdP

- Service account in sharedidp master realm for portal backend to call Keycloak (portal helm chart: backend.keycloak.shared.clientId)
    - client id: sa-cl1-reg-1
    - client secret: YPA1t6BMQtPtaG3fpH8Sa8Ac6KYbPUM7
