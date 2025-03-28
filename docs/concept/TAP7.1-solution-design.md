# [TAP 7.1] Solution Design Hausanschluss Bundle Konzept

# 1 Business Case

## 1.1 Executive Summary

The EDC "Hausanschluss" Bundle aims to simplify the installation of the enablement services Eclipse Dataspace
Connector (EDC), Digital Twin Registry (DTR), and their supporting components. By developing a flexible, parameterizable
installation package, the project seeks to reduce deployment complexity and lower barriers to participation in the
Catena‑X data space. This bundle will enable independent component updates and support a modular "bring your own"
approach, ultimately fostering a more efficient and accessible ecosystem for diverse participants—such as testers,
external developers, and small and medium-sized enterprises.

## 1.2 Business Need

Current deployment methods for data space integration are complex and require significant manual effort. This PoC
addresses the need to:

- Reduce Complexity: Simplify the deployment topology by bundling components into capabilities.
- Automate Deployment: Provide an automated installation package using Kubernetes and HELM.
- Reduce Configuration Efforts: Streamline and reduce the number of configuration steps required for integration.
- Extend Documentation: Provide a detailed documentation tailored to the target groups.
- Enable Extension: Design the system to allow the seamless addition of new components or capabilities.

## 1.3 Objectives

- Simplify Deployment and Maintenance: Develop an installation package that minimizes manual configuration through
  automation.
- Ensure Modularity: Structure the bundle so that components can be independently installed, updated, or replaced
  without
  affecting other services.
- Facilitate Flexibility: Implement a "bring your own" model for key components, such as EDC, PostgreSQL, and HashiCorp
  Vault, to allow tailored deployments that meet specific needs.
- Increase Accessibility: Lower entry barriers for new participants by reducing technical complexity and operational
  dependencies.
- Scalability: Structure the bundle so that it can be deployed multiple times.

## 1.4 Expected Deliverables

- PoC Documentation: A concept and architecture overview highlighting the modular design.
- Modular Installation Package: A set of HELM charts for deploying the enablement service bundles:
    - EDC Bundle: Including the Eclipse Dataspace Connector, EDC PostgreSQL, and HashiCorp Vault.
    - Digital Twin Bundle: Featuring components such as the Decentral DT Registry (with “bring your own” PostgreSQL) and
      a Submodel Server Bundle.
    - Identity Wallet Bundle: Covering the Identity Wallet functionality.
- Demonstration Environment: A test deployment showcasing reduced complexity and improved efficiency.
- Basic User Guide: Instructions on how to deploy and update the PoC bundle.

## 1.5 Benefits

- Operational Efficiency: Faster and more reliable deployments with less manual work.
- Scalability: A modular design that can be scaled or adapted for future full-scale deployments.
- Ease of Adoption: Simplified deployment processes make it easier for testers and external developers to engage.

## 1.6. Dependencies

- Interoperability with the CATENA‑X standards.

## 1.7. Success Criteria

- Technology Readiness Level: Achievement of a Technology Readiness Level (TRL) of 3, as specified in the requirements.
- Functional PoC Deployment: Demonstrated automated, modular installation with reduced manual steps.
- Simplified Configuration: Clear evidence of reduced configuration complexity.
- Positive Feedback: End-user validation from a select group of demo participants and the Tractus-X community.
- Documentation Completeness: Availability of concise deployment and user guides.

## 1.8. Out of Scope

- Full Production Readiness: This PoC is not intended to be a production-ready solution.
- Core Services Exclusion: Core services are not part of the Hausanschluss Bundles.
- App Provider Role: The role of App Provider is considered out of scope for this deployment.
- Alternative Deployment Techniques: While the evaluation of alternative deployment methods is acknowledged, the primary
  focus remains on Kubernetes and HELM-based deployment.

# 2 Requirements Analysis

## 2.1 Assumptions

## 2.2 Requirements Catalog

| ID             | Requirement                                                                                                                                                                                                                                                                                                                                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Deliverables / Acceptance Criteria                                                                                                           |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| [WP-7.1.-D001] | TAP7.1 Hausanschluss Bundle aims to simplify the installation and maintenance of the EDC and other components that together ensure a “home connection”. A flexible, parameterizable installation package is intended to reduce complexity and make integration more efficient, thereby simplifying participation in Catena‑X for additional participants. | Specification and development of a flexible, parameterizable installation package that reduces the complexity of installing and maintaining the required components for seamless integration into the Catena‑X data space. This package should facilitate updates and new versions, making participation in Catena‑X more efficient and accessible. In doing so, SMEs shall be enabled to participate without high costs or dependency on SaaS providers while maintaining control over their IT infrastructure. | [WP-7.1.-D001] Concept for the Hausanschluss is created                                                                                      |
| 7.1.1.1        | The solution concept must define the Capability Bundles structures to be implemented. For each Capability Bundle, the included bundles and their versions are mapped.                                                                                                                                                                                     | "The following Capability Bundle structure is implemented:                                                                                                                                                                                                                                                                                                                                                                                                                                                       | "The structure of the Capability Bundles for the Enablement Services has been specified.                                                     |
| 7.1.1.2        | Definition of Data Space Roles                                                                                                                                                                                                                                                                                                                            | Capability EDC (Data Transfer) Bundle                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | For version R24.12 it is clearly defined which Tractus‑X services and components are assigned to each Capability Bundle"                     |
| 7.1.1.4        | Modularity & Maintainability: No dependencies between Capability Bundles                                                                                                                                                                                                                                                                                  | Eclipse Dataspace Connector (EDC) v0.9.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | "As part of the target group analysis, the target groups are defined and aligned with the data space roles.                                  |
| 7.1.1.5        | Modularity & Maintainability: Concept for reducing deployment complexity                                                                                                                                                                                                                                                                                  | EDC PostgresSQL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Mapping from data space role to target group has been completed.                                                                             |
| 7.1.1.6        | Modularity & Maintainability                                                                                                                                                                                                                                                                                                                              | HashiCorp Vault                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Mapping from target group to data space role has been completed.                                                                             |
| 7.1.1.13       | Solution Concept                                                                                                                                                                                                                                                                                                                                          | Capability Digital Twin Bundle                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | An assignment of data space roles to Capability Bundles has been made."                                                                      |
| 7.1.1.14       | Scalability of Enablement Services                                                                                                                                                                                                                                                                                                                        | Decentral DT Registry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | "Components and Services should obly be part of one bundle.                                                                                  |
| 7.1.1.16       | Interoperability                                                                                                                                                                                                                                                                                                                                          | PostgresSQL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Each bundle must be deployable in isolation and can be installed, updated, or removed independently.                                         |
| [WP-7.1.-D002] | [WP-7.1.-D002] Target group for the specification is defined.                                                                                                                                                                                                                                                                                             | Capability Identity & Trust (Identity Wallet Bundle)                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Capability Bundles must be organized in separate HELM sub‑charts.                                                                            |
| 7.1.2.1        | Target Group Analysis                                                                                                                                                                                                                                                                                                                                     | Identity Wallet Mock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Circular dependencies between bundles must be avoided."                                                                                      |
| [WP-7.1.-D003] | [WP-7.1.-D003] Decentralized components and services defined                                                                                                                                                                                                                                                                                              | Capability Semantic Model Bundle                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | "Simplification of deployment processes                                                                                                      |
| 7.1.3.1        | See [WP-7.1.-D001-AC001]                                                                                                                                                                                                                                                                                                                                  | Submodel Mock (aus Umbrella HELM Chart)"                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | A reduction of manual configuration steps has been achieved.                                                                                 |
| [WP-7.1.-D004] | [WP-7.1.-D004] Documentation of the Hausanschluss Bundle is completed                                                                                                                                                                                                                                                                                     | "Data Consumer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Transparency and traceability                                                                                                                |
| 7.1.4.1        | Documentation of the Hausanschluss-Bundles                                                                                                                                                                                                                                                                                                                | Data Provider                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Clearly documented deployment steps are provided.                                                                                            |
| 7.1.4.2        | Documentation of the Hausanschluss-Bundles                                                                                                                                                                                                                                                                                                                | Enablement Service Provider"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Improvements of Chart configuration by                                                                                                       |
| [WP-7.1.-D005] | [WP-7.1.-D005] Umbrella HELM Charts for the Hausanschluss developed, tested, and documented                                                                                                                                                                                                                                                               | "Unique assignment of components and services to a defined Capability Bundle.                                                                                                                                                                                                                                                                                                                                                                                                                                    | usage of template                                                                                                                            |
| 7.1.5.1        | Re-activate Umbrella HELM Charts to the latest release state                                                                                                                                                                                                                                                                                              | Each component and service should be assigned to only one Capability Bundle.                                                                                                                                                                                                                                                                                                                                                                                                                                     | reducing configuration options                                                                                                               |
| 7.1.5.2        | Hierarchical structuring and bundling of Enablement Service components in the Umbrella HELM Chart                                                                                                                                                                                                                                                         | Dependencies between Capability Bundles are allowed."                                                                                                                                                                                                                                                                                                                                                                                                                                                            | reducing manual steps in the setup"                                                                                                          |
| 7.1.5.3        | Interchangeability of bundle components via “Bring-Your-Own” components                                                                                                                                                                                                                                                                                   | The system deployment should be optimized to reduce the existing complexity. The goal is to make the provisioning process more efficient, robust, and easier to maintain.                                                                                                                                                                                                                                                                                                                                        | Charts are published via a publicly accessible charts repository.                                                                            |
| [WP-7.1.-D006] | [WP-7.1.-D006] Product developed according to a Technology Readiness Level (TRL) of 3                                                                                                                                                                                                                                                                     | Charts are published automatically.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | "The solution design for the ""Hausanschluss"" Bundle is created.                                                                            |
| 7.1.6.1        | POC                                                                                                                                                                                                                                                                                                                                                       | Creation of a solution design for the “Hausanschluss” Bundle.                                                                                                                                                                                                                                                                                                                                                                                                                                                    | The solution design for the ""Hausanschluss"" Bundle ispublished in the repository: https://github.com/eclipse-tractusx/tractus-x-umbrella." |
| 7.1.6.2        | Deployment Strategy                                                                                                                                                                                                                                                                                                                                       | Scalability of Enablement Services                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | "Developers should be able to deploy an arbitrary number of Enablement Services.                                                             |

# 3 AS-IS Analysis

## 3.1 People

### 3.1.1 Target Group Analysis

See "4.1.1 To-be Target Group Analysis" below. No deviations between As-is and To-be target groups have been identified.

## 3.2 Process

### 3.2.1 Use Case View (high-level)

Umbrella Chart is intended for the following Use Cases:

| Actor             | Use case                                                                                             |
|-------------------|------------------------------------------------------------------------------------------------------|
| Product Developer | Sandbox Environments: Create local environments to evaluate and experiment with Catena-X components. |
| Product Developer | Development: Provide a unified setup for contributors and developers working on Tractus-X projects.  |
| Product Tester    | Testing: Run end-to-end tests for Catena-X services.                                                 |

## 3.4 System

### 3.4.1 Context Delimitation

````mermaid
flowchart
    subgraph "Umbrella Chart"
        ChartYaml["Chart.yaml"]
        subgraph charts
            Portal["Portal"]
            CentralIdp["CentralIdp"]
            DiscoveryFinder["Discovery Finder"]
            SDFactory["SD-Factory"]
            SSICredentialIssuer["SSI Credential Issuer"]
            SemanticHub["Semantic Hub"]
            BPDM["BPDM"]
            DataConsumer["Data Consumer"]
            DataProvider["Data Provider"]
            BDRS["BDRS"]
            SSIWalletStub["SSI Wallet Stub"]
        end
        subgraph "tx-data-provider"
            EDC["EDC"]
            DTR["DTR"]
            SubmodelServer["Submodel Server"]
        end
    end

    ChartYaml --> Portal
    ChartYaml --> CentralIdp
    ChartYaml --> DiscoveryFinder
    ChartYaml --> SDFactory
    ChartYaml --> SSICredentialIssuer
    ChartYaml --> SemanticHub
    ChartYaml --> BPDM
    ChartYaml --> DataConsumer
    ChartYaml --> DataProvider
    ChartYaml --> BDRS
    ChartYaml --> SSIWalletStub
    DataConsumer --> EDC
    DataProvider --> EDC
    DataProvider --> DTR
    DataProvider --> SubmodelServer
````

#### Existing Umbrella Chart Structure

# 4 TO-BE Design

## 4.1 People

### 4.1.1 Target Group Analysis

Overall data space roles: https://catena-x.net/en/1/catena-x-introduce-implement/how-to-operate-catena-x

The relevant data space roles for us under requirement 7.1.1.1 are:

- Data Consumer
- Data Provider
- Enablement Service Provider

Scope: Umbrella HELM Charts

- Enablement Services: These services are included under the umbrella of HELM charts, focusing on enabling
  functionalities.
- Out of Scope: Core services such as Portal or BPDM are not considered within this scope.

Primary target groups:

| No. | Target group                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Data space roles                                                    | Target group differentiation                                                                                                                                                                                                                                                                            | Behaviour, Needs, Pains & Usage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Developers<ul><li>External Developers (not Tractus-X developers): Utilize the chart for demonstration or evaluation purposes.</li><li>Experienced software and product developers who are developing a business app for a CATENA-X data space. They need to develop the app against the interfaces of the data space and integrate them accordingly.</li><li>They emphasize efficient and cost-effective implementation:<ul><li>Cost Efficiency: They do not want to use expensive SaaS solutions.</li><li>Technical Independence: They lack the knowledge and capacity to deploy the enablement and core services of the data space themselves.</li><li>Focus on Development: They concentrate on application development without delving deeply into the deployment and operation of the underlying infrastructure.</li></ul></li><li>Out of Scope: Developers running tests in test runners are not considered within this scope.</li></ul> | Data Consumer <br/> Data Provider <br/> Enablement Service Provider |                                                                                                                                                                                                                                                                                                         | <ul><li>Needs / sources of information<ul><li><a href="https://eclipse-tractusx.github.io/Kits/">Kit documentation tractus-x</a> for interaction purposes</li><li><a href="https://catenax-ev.github.io/">Catena-X doucmentation</a> for standards and regulations</li><li><a href="https://github.com/eclipse-tractusx/tractus-x-umbrella">Umbrella documentation</a> for umbrella component information</li></ul></li><li>Challenges → Solution<ul><li>Decentralization e.g. Where are other systems? How to interact with them? → Solution: Umbrella charts and bundles for deployment</li><li>Complex setup → Solution: delivery of small capability bundles</li></ul></li></ul> |
| 2   | <ul><li>Tester requiring a test system (Testmanagement e.V.)</li><li>Requirement: Testbed</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Data Consumer <br/> Data Provider <br/> Enablement Service Provider | <ul><li>Developer (1) tests their feature.</li><li>Tester (2) performs end-to-end testing.</li><li>For the tester, the modular structure is less relevant since they focus on E2E testing, whereas the developer selects the required components.</li><li>The testbed must be easy to deploy.</li></ul> | <ul><li>Same as above from an End-to-end testing perspective</li><li>Typically a tester has less technical know-how than a developer and therefore needs a "one-size-fits-all" chart for easier testing</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## 4.2 Process

### 4.2.1 Use Case View (high-level)

| Use Case                                | Description                                                                                                       | Actors            |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------|-------------------|
| Configure HELM Chart                    | The product developer configures the HELM Chart for the specific environment.                                     | Product Developer |
| Configure Secrets                       | The product developer manages and configures secrets.                                                             | Product Developer |
| Execute Deployment Pipeline             | The product developer successfully executes the deployment pipeline for the HELM Chart.                           | Product Developer |
| Integrate EDC, DTR, and Identity Wallet | The actors integrate the components EDC, Digital Twin Registry, and Identity Wallet for seamless interoperability | Product Developer |
| Set Up Connection Infrastructure        | The actor sets up the connection infrastructure for linking to the central data space infrastructure.             | Product Developer |
| Maintain Infrastructure Module          | The product developer maintains the modular architecture of the HELM Chart.                                       | Product Developer |
| Ensure Scalability                      | The product developer ensures scalability to support growing numbers of users and data volumes.                   | Product Developer |
| A/B Testing                             | The product tester executes A/B tests.                                                                            | Product Tester    |

### 4.2.2 Business Process (SCC Artifact)

#### Chart Release Process

Charts will be released using the already existing workflow in the Umbrella Chart repository. The workflow will
automatically release a Chart, once it is pushed to the "charts/" directory with a new Chart version.

#### Capability Bundle Structure

Capability bundle modularization for the Tractus-X Umbrella Helm chart is a sound architectural and operational design.
It aligns with both the domain-driven architecture of Catena-X (data exchange, digital twin, identity, semantics are
distinct domains) and with Kubernetes best practices for managing complex applications (using an umbrella chart to
bundle related microservices).

Each bundle is self-sufficient, which improves isolation (failures or changes in one domain have minimal impact on
others) and allows scaling and upgrading along domain lines. It simplifies deployment by allowing “plug-and-play”
capabilities: an Enablement Service Provider can decide which bundles to operate based on its role e.g., include the
Digital Twin and Semantic bundles if offering an asset-rich service, or omit them if not. The approach is consistent
with how other OSS projects deliver multi-component systems, providing one-step installation without sacrificing the
ability to tweak individual parts.

Why this structure was proposed:

1. **Clear Separation of Concerns**  
   Each capability bundle (e.g. EDC Data Transfer, Digital Twin, Identity & Trust, Semantic Model) aligns with a
   specific functional domain. This separation makes it easier to understand the role of each service (e.g., the EDC
   connector vs. the digital twin registry), reduces coupling between unrelated components, and ultimately makes
   maintenance and troubleshooting more straightforward.
2. **Modular Deployment**  
   Some participants in Catena-X may not need all services (e.g., some might not use the Digital Twin bundle). By
   structuring the umbrella chart into bundles, a user can enable just those needed capabilities. This leads to leaner
   installs and avoids unnecessary resource usage.
3. **Best Practices with Helm**  
   Using an umbrella chart with subcharts/bundles is a well-recognized Helm best practice for complex applications. It
   allows a single helm install to set up multiple microservices while still allowing each service to have its own
   lifecycle, configuration, and version.
4. **Alignment with Domain-Driven Approach**  
   Catena-X is organized around distinct, loosely-coupled “building blocks.” Bundling services by domain matches this
   architectural vision. It’s clear which domain each set of microservices belongs to (EDC for data exchange, identity
   for credential management, etc.). This clarity also helps new adopters navigate the ecosystem.

````mermaid
flowchart LR
    subgraph "Core Services"
        Vault["Vault"]
    end

    subgraph "Capability Bundle: Identity & Trust"
        SSIWalletStub["SSI Wallet Stub"]
    end

    subgraph "Capability Bundle: Dataspace Connector"
        EDC["EDC"]
        EDCDB["EDC DB"]
    end

    subgraph "Capability Bundle: Digital Twin"
        DTR["DTR"]
        DTRDB["DTR DB"]
    end

    subgraph "Capability Bundle: Data Persitence Layer"
        SimpleSubmodelServer["Simple Submodel Server"]
    end

    subgraph "Hausanschluss Bundles"
        subgraph "Data Provider"
            DataProvider["Data Provider"]
        end
        subgraph "Data Consumer"
            DataConsumer["Data Consumer"]
        end
        subgraph "Enablement Provider"
            EnablementProvider["Enablement Provider"]
        end
    end

    EDC -.-> SSIWalletStub
    EDC -.-> Vault
    DataProvider --> EDC
    DataProvider --> DTR
    DataProvider --> SimpleSubmodelServer
    DataConsumer --> EDC
    EnablementProvider --> DataConsumer
    EnablementProvider --> DataProvider

````

#### Deployment strategies

##### Role: Data Provider

The standard data provider role consists of a EDC, DTR and Submodel Server Bundles. EDC uses the Identity Wallet Bundle.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Data Persistence Layer"]
    C["Capability Bundle: Dataspace Connector"]
    D["Capability Bundle: Digital Twin"]
    E["Application to be tested/developed"]
    E --> B
    E --> C
    E --> D
    C --> A
````

##### Role: Data Consumer

The standard data consumer role consists of only the EDC Bundle and the Identity Wallet Bundle.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Dataspace Connector"]
    C["Application to be tested/developed"]
    C --> B
    B --> A

````

##### Role: Enablement Provider

The Enablement Provider roles consists of both the Data Consumer and Data Provider bundles. This allows provisioning of
data and the consumtion of the provisioned data by a application.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Data Persitance Layer"]
    C["Application to be tested/developed"]
    D["Capability Bundle: Digital Twin"]
    E["Capability Bundle: Dataspace Connector (Provider)"]
    F["Capability Bundle: Dataspace Connector (Consumer)"]
    C --> B
    C --> D
    C --> E
    C --> F
    E --> A
    F --> A
````

##### Bring you own

Each Bundle can be deactivated to use your own component. This requires configuration of the component specific
parameters in the other components.

In this example this would be the configuration of the Identity Wallet within the EDC.

````mermaid
flowchart BT
    A["Application to be tested/developed"]
    B["Capability Bundle: Dataspace Connector"]
    C["<s>Capability Bundle: Identity & Trust</s>"]
    D["Own Identity Wallet"]
    A --> B
    B -- identitywallet - bundle . enabled = false --> C
    B -- configure --> D

````

## 4.4 System

### 4.4.1 Context Delimitation / 4.4.2 Interface Documentation

````mermaid
flowchart LR
    Dataprovider["Dataprovider"] -->|stores data| SubmodelServer["Submodel Server"]
    Dataprovider -->|creates twins| DTR["DTR"]
    Dataprovider -->|creates contracts| EDC["EDC"]
    Dataconsumer["Dataconsumer"] -->|negotiate contracts| EDC
    DTR -->|needs| IdentityWallet["Identity Wallet"]
    IdentityWallet -->|needs| Postgres["PostgreSQL Database"]
````

# 5 Build

## 5.1 DevOps Setup Definition

### 5.1.1 Tool Chain Definition

##### Version Control & Source Code Management

- **Git & GitHub**: Management of the source code, the Helm Charts, and associated documentation in a centralized
  repository.

##### Build and CI/CD Tools

- **GitHub Actions**: Automated workflows for linting, testing, packaging, and releasing the Helm Charts.
- **Helm CLI**: For validating, packaging, and deploying the charts.
- **Helm Lint**: Performing static analyses to ensure compliance with chart standards.

##### Testing and Validation Tools

- **chart-testing Tool**: Validation of the Helm Charts based on Kubernetes schemas.
- **Local Cluster Tests**: Use of tools such as Kind or Minikube to perform integration tests in a test environment.

##### Release Management & Deployment

- **Chart Releaser**: Automated creation and publication of chart releases.
- **Helm Chart Repository / GitHub Packages**: Hosting and provisioning of the finalized charts.

# NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>