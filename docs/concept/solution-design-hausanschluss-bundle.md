# Solution Design "Hausanschluss" Bundle Concept

<!-- TOC -->
* [Solution Design "Hausanschluss" Bundle Concept](#solution-design-hausanschluss-bundle-concept)
* [1 Business Case](#1-business-case)
  * [1.1 Executive Summary](#11-executive-summary)
  * [1.2 Business Need](#12-business-need)
  * [1.3 Objectives](#13-objectives)
  * [1.4 Expected Deliverables](#14-expected-deliverables)
  * [1.5 Benefits](#15-benefits)
  * [1.6. Dependencies](#16-dependencies)
  * [1.7. Success Criteria](#17-success-criteria)
  * [1.8. Out of Scope](#18-out-of-scope)
* [2 Requirements Analysis](#2-requirements-analysis)
  * [2.1 Requirements Catalog](#21-requirements-catalog)
* [3 AS-IS Analysis](#3-as-is-analysis)
  * [3.1 People](#31-people)
    * [3.1.1 Target Group Analysis](#311-target-group-analysis)
  * [3.2 Process](#32-process)
    * [3.2.1 Use Case View (high-level)](#321-use-case-view-high-level)
  * [3.3 System](#33-system)
    * [3.3.1 Context Delimitation](#331-context-delimitation)
      * [Existing Umbrella Chart Structure](#existing-umbrella-chart-structure)
* [4 TO-BE Design](#4-to-be-design)
  * [4.1 People](#41-people)
    * [4.1.1 Target Group Analysis](#411-target-group-analysis)
      * [Scope: Umbrella HELM Charts](#scope-umbrella-helm-charts)
      * [Out of Scope:](#out-of-scope)
      * [Primary target groups:](#primary-target-groups)
  * [4.2 Process](#42-process)
    * [4.2.1 Use Case View (high-level)](#421-use-case-view-high-level)
      * [Group 1: Product developer](#group-1-product-developer)
      * [Group 2: Product Tester](#group-2-product-tester)
      * [Group 3: Product Manager](#group-3-product-manager)
      * [Use Case diagram](#use-case-diagram)
    * [4.2.2 Business Process (SCC Artifact)](#422-business-process-scc-artifact)
      * [Chart Release Process](#chart-release-process)
      * [Capability Bundle Structure](#capability-bundle-structure)
        * [Core Principles](#core-principles)
        * [Benefits](#benefits)
      * [Deployment strategies](#deployment-strategies)
        * [Role: Data Provider](#role-data-provider)
        * [Role: Data Consumer](#role-data-consumer)
        * [Role: Enablement Provider](#role-enablement-provider)
      * [Bring your own](#bring-your-own)
      * [Scalability](#scalability)
      * [Interoperability](#interoperability)
    * [4.2.2.1 Reduction of Complexity in the Deployment Process](#4221-reduction-of-complexity-in-the-deployment-process)
      * [1. Standardization of Bundle Configuration](#1-standardization-of-bundle-configuration)
      * [2. Automated Validation & Linting in CI](#2-automated-validation--linting-in-ci)
      * [3. Reduction of configuration steps](#3-reduction-of-configuration-steps)
      * [4. CLI or Script Support for Custom Deployments](#4-cli-or-script-support-for-custom-deployments)
      * [5. Dynamic Naming for Multiple Deployments](#5-dynamic-naming-for-multiple-deployments)
      * [6. Documentation & Visibility](#6-documentation--visibility)
  * [4.3 System](#43-system)
    * [4.3.1 Context Delimitation / 4.3.2 Interface Documentation](#431-context-delimitation--432-interface-documentation)
* [5 Build](#5-build)
  * [5.1 DevOps Setup Definition](#51-devops-setup-definition)
    * [5.1.1 Tool Chain Definition](#511-tool-chain-definition)
        * [Version Control & Source Code Management](#version-control--source-code-management)
        * [Build and CI/CD Tools](#build-and-cicd-tools)
        * [Testing and Validation Tools](#testing-and-validation-tools)
        * [Release Management & Deployment](#release-management--deployment)
* [NOTICE](#notice)
<!-- TOC -->

# 1 Business Case

## 1.1 Executive Summary

The "Hausanschluss" Bundle aims to simplify the installation of the enablement services Eclipse Dataspace
Connector (EDC), Digital Twin Registry (DTR), and their supporting components. By developing a flexible, parameterizable
installation package, the project seeks to reduce deployment complexity and lower barriers to participation in the
Catena‑X data space. This bundle will enable independent component updates and support a modular "bring your own"
approach, ultimately fostering a more efficient and accessible ecosystem for diverse participants—such as testers,
external product developers, product testers, and small and medium-sized enterprises.

## 1.2 Business Need

Current deployment methods for data space integration are complex and require significant manual effort. This PoC
addresses the need to:

- **Reduce Complexity:** Simplify the deployment topology by bundling components into capabilities.
- **Automate Deployment:** Provide an automated installation package using Kubernetes and HELM.
- **Minimize Configuration Overhead:** Streamline the integration process by providing pre-configured bundles that
  require only minimal manual parameter adjustments.
- **Extend Documentation:** Provide a detailed documentation tailored to the target groups.
- **Enable Extension:** Design the system to allow the seamless addition of new components or capabilities.

## 1.3 Objectives

- **Simplify Deployment and Maintenance:** Develop an installation package that minimizes manual configuration through
  automation.
- **Ensure Modularity:** Structure the bundle so that components can be independently installed, updated, or replaced
  without affecting other services.
- **Facilitate Flexibility:** Implement a "bring your own" model for key components, such as EDC, PostgreSQL, and
  HashiCorp Vault, to allow tailored deployments that meet specific needs.
- **Increase Accessibility**: Lower entry barriers for new participants by reducing technical complexity and operational
  dependencies.
- **Scalability:** Structure the bundles so that they can be deployed multiple times.

## 1.4 Expected Deliverables

- **[PoC Documentation](/docs/concept/solution-design-hausanschluss-bundle.md):** A concept and architecture overview highlighting the modular design.
- **Modular Installation Package:** A set of HELM charts for deploying the enablement service bundles:
    - **[Dataspace Connector Bundle](/charts/dataspace-connector-bundle):** Including the Eclipse Dataspace Connector, EDC PostgreSQL, and HashiCorp Vault.
    - **[Digital Twin Bundle](/charts/digital-twin-bundle):** Featuring components such as the Decentral DT Registry (with “bring your own” PostgreSQL).
    - **[Data Persistence Layer Bundle](/charts/data-persistence-layer-bundle):** Including a simple Submodel Server to store semantic data.
    - **[Identity & Trust Bundle](/charts/identity-and-trust-bundle)**: Covering the Identity Wallet functionality.
- **Demonstration Environment:** A test deployment showcasing reduced complexity and improved efficiency.
- **[Basic User Guide](/docs/user/guides/hausanschluss-bundles.md):** Instructions on how to deploy and update the PoC bundle

## 1.5 Benefits

- **Operational Efficiency:** Faster and more reliable deployments with less manual work.
- **Scalability:** A modular design that can be scaled or adapted for future full-scale deployments.
- **Ease of Adoption:** Simplified deployment processes make it easier for testers and external developers to engage.

## 1.6. Dependencies

- **Interoperability** with the CATENA‑X standards.

## 1.7. Success Criteria

- **Technology Readiness Level:** Achievement of a Technology Readiness Level (TRL) of 3, as specified in the
  requirements.
- **Functional PoC Deployment:** Demonstrated automated, modular installation with reduced manual steps.
- **Simplified Configuration:** Clear evidence of reduced configuration complexity.
- **Positive Feedback:** End-user validation from a select group of demo participants and the Tractus-X community.
- **Documentation Completeness:** Availability of concise deployment and user guides.

## 1.8. Out of Scope

- **Full Production Readiness:** This PoC is not intended to be a production-ready solution.
- **Core Services Exclusion:** Core services are not part of the Hausanschluss Bundles.
- **App Provider Role:** The role of App Provider is considered out of scope for this deployment.
- **Alternative Deployment Techniques:** While the evaluation of alternative deployment methods is acknowledged, the
  primary focus remains on Kubernetes and HELM-based deployment.

# 2 Requirements Analysis

## 2.1 Requirements Catalog

| ID             | Requirement                                                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Deliverables / Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                                   |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [WP-7.1.-D001] | The Hausanschluss Bundle aims to simplify the installation and maintenance of the EDC and other components that together ensure a “Hausanschluss”. A flexible, parameterizable installation package is intended to reduce complexity and make integration more efficient, thereby simplifying participation in Catena‑X for additional participants. | Specification and development of a flexible, parameterizable installation package that reduces the complexity of installing and maintaining the required components for seamless integration into the Catena‑X data space. This package should facilitate updates and new versions, making participation in Catena‑X more efficient and accessible. In doing so, SMEs shall be enabled to participate without high costs or dependency on SaaS providers while maintaining control over their IT infrastructure. | [WP-7.1.-D001] Concept for the Hausanschluss is created                                                                                                                                                                                                                                                                                                                                                              |
| 7.1.1.1        | The solution concept must define the Capability Bundles structures to be implemented. For each Capability Bundle, the included bundles and their versions are mapped.                                                                                                                                                                                | The following Capability Bundle structure is implemented:                                                                                                                                                                                                                                                                                                                                                                                                                                                        | The structure of the Capability Bundles for the Enablement Services has been specified. For version R24.12 it is clearly defined which Tractus‑X services and components are assigned to each Capability Bundle                                                                                                                                                                                                      |
| 7.1.1.2        | Definition of Data Space Roles                                                                                                                                                                                                                                                                                                                       | Data Consumer, Data Provider, Enablement Service Provider                                                                                                                                                                                                                                                                                                                                                                                                                                                        | As part of the target group analysis, the target groups are defined and aligned with the data space roles. <br>Mapping from data space role to target group has been completed. <br>Mapping from target group to data space role has been completed. <br>An assignment of data space roles to Capability Bundles has been made.                                                                                      |
| 7.1.1.4        | Modularity & Maintainability: Components and services must be assigned to a single Capability Bundle.                                                                                                                                                                                                                                                | Assignment of components and services to a defined Capability Bundle. <br>Each component and service should be assigned to only one Capability Bundle. <br>Dependencies between Capability Bundles are allowed.                                                                                                                                                                                                                                                                                                  | Components and Services should only be part of one bundle. <br>Each bundle must be deployable in isolation and can be installed, updated, or removed independently. <br>Capability Bundles must be organized in separate HELM sub‑charts. <br>Circular dependencies between bundles must be avoided.                                                                                                                 |
| 7.1.1.5        | Modularity & Maintainability: Concept for reducing deployment complexity                                                                                                                                                                                                                                                                             | The system deployment should be optimized to reduce the existing complexity. The goal is to make the provisioning process more efficient, robust, and easier to maintain.                                                                                                                                                                                                                                                                                                                                        | **Simplification of deployment processes:** A reduction of manual configuration steps has been achieved. <br>**Transparency and traceability:** Clearly documented deployment steps are provided. <br>**Improvements of Chart configuration by:** <br>usage of template  <br>reducing configuration options <br>reducing manual steps in the setup                                                                   |
| 7.1.1.6        | Modularity & Maintainability                                                                                                                                                                                                                                                                                                                         | Charts are published automatically.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Charts are published via a publicly accessible charts repository.                                                                                                                                                                                                                                                                                                                                                    |
| 7.1.1.13       | Solution Concept                                                                                                                                                                                                                                                                                                                                     | Creation of a solution design for the “Hausanschluss” Bundle.                                                                                                                                                                                                                                                                                                                                                                                                                                                    | The solution design for the "Hausanschluss" Bundle is created. <br>The solution design for the "Hausanschluss" Bundle is published in the repository: https://github.com/eclipse-tractusx/tractus-x-umbrella.                                                                                                                                                                                                        |
| 7.1.1.14       | Scalability of Enablement Services                                                                                                                                                                                                                                                                                                                   | Scalability of Enablement Services                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Developers should be able to deploy an arbitrary number of Enablement Services. <br>Example: Up to 3 EDCs can be provided.                                                                                                                                                                                                                                                                                           |
| 7.1.1.16       | Interoperability                                                                                                                                                                                                                                                                                                                                     | Interoperability                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Interoperability with the CATENA‑X standards. <br>This interoperability is documented and traceable.                                                                                                                                                                                                                                                                                                                 |
| [WP-7.1.-D002] | [WP-7.1.-D002] Target group for the specification is defined.                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [WP-7.1.-D002] Target group for the specification is defined.                                                                                                                                                                                                                                                                                                                                                        |
| 7.1.2.1        | Target Group Analysis                                                                                                                                                                                                                                                                                                                                | The target group analysis for the "Hausanschluss Bundle"is defined.                                                                                                                                                                                                                                                                                                                                                                                                                                              | The analysis has been conducted. <br>The target group is included in the solution concept <br>To be clarified: What is included in the Hausanschluss and who can operate it in which scenario (OEM, SME, service provider, etc.).                                                                                                                                                                                    |
| [WP-7.1.-D003] | [WP-7.1.-D003] Decentralized components and services defined                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [WP-7.1.-D003] Decentralized components and services have been defined.                                                                                                                                                                                                                                                                                                                                              |
| 7.1.3.1        | See [WP-7.1.-D001-AC001]                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | See [WP-7.1.-D001-AC001]                                                                                                                                                                                                                                                                                                                                                                                             |
| [WP-7.1.-D004] | [WP-7.1.-D004] Documentation of the Hausanschluss Bundle is completed                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [WP-7.1.-D004] Documentation of the Hausanschluss Bundle is completed                                                                                                                                                                                                                                                                                                                                                |
| 7.1.4.1        | Documentation of the Hausanschluss-Bundles                                                                                                                                                                                                                                                                                                           | Usability                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Documentation is provided that enables an experienced product developer - with knowledge of Helm Charts, Docker, and Vaults - to deploy the chart independently without external help. <br>A troubleshooting and FAQ section is included to support the developer. <br>Prerequisites, skills, and technology requirements are outlined, detailing what a developer must know to perform the deployment autonomously. |
| 7.1.4.2        | Documentation of the Hausanschluss-Bundles                                                                                                                                                                                                                                                                                                           | Documentation of the Hausanschluss-Bundles is completed.                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Documentation is provided for: <br>Configuration of the defined bundles according to the specified requirements and parameters. <br>Integration of the documentation into the Umbrella HELM Charts. <br>Integration into the Umbrella HELM Chart to ensure consistent deployment.                                                                                                                                    |
| [WP-7.1.-D005] | [WP-7.1.-D005] Umbrella HELM Charts for the Hausanschluss developed, tested, and documented                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [WP-7.1.-D005] Umbrella HELM Charts for the Hausanschluss have been developed, tested, and documented.                                                                                                                                                                                                                                                                                                               |
| 7.1.5.1        | Re-activate Umbrella HELM Charts to the latest release state                                                                                                                                                                                                                                                                                         | The Enablement Services components of the Umbrella HELM Charts must be updated to version R24.12. This includes the following upgrades: <br> Upgrade DTR to version R24.12 (#188) <br>Upgrade EDCs to version R24.12 (#193) <br>Update SSI-DIM-Wallet-Stub to version 0.1.8 (#206)                                                                                                                                                                                                                               | The HELM Chart will then contain the updated versions of the components. <br>After the upgrade, the components (DTR, EDCs, SSI‑DIM‑Wallet‑Stub) run stably without functional impairments. <br>The deployment pipeline for the HELM Chart executes successfully. <br>Relevant tests & smoke tests (e.g., integration tests) confirm the migration.                                                                   |
| 7.1.5.2        | Hierarchical structuring and bundling of Enablement Service components in the Umbrella HELM Chart                                                                                                                                                                                                                                                    | The Umbrella HELM Chart should be structured hierarchically so that related Enablement Service components are grouped into bundles. <br>The Umbrella HELM Chart must have a clear hierarchical structure. <br> Each Enablement Service component must be assigned to a unique bundle.<br>No circular dependencies between bundles are allowed.                                                                                                                                                                   | The chart is modular and divided into defined bundles. <br>Each bundle can be deployed and maintained independently.                                                                                                                                                                                                                                                                                                 |
| 7.1.5.3        | Interchangeability of bundle components via “Bring-Your-Own” components                                                                                                                                                                                                                                                                              | Bundle components should be interchangeable through “Bring-Your-Own” components. <br>“Bring your own” is available for every component and means that these components do not have to be delivered by default with the Umbrella Chart but can be provided by the respective users.                                                                                                                                                                                                                               | Bundle components can be interchanged by “Bring-Your-Own” components.                                                                                                                                                                                                                                                                                                                                                |
| [WP-7.1.-D006] | [WP-7.1.-D006] Product developed according to a Technology Readiness Level (TRL) of 3                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | [WP-7.1.-D006] The product is developed according to a Technology Readiness Level (TRL) of 3                                                                                                                                                                                                                                                                                                                         |
| 7.1.6.1        | POC                                                                                                                                                                                                                                                                                                                                                  | Creation of a POC for the "Hausanschluss" Bundle                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | POC implementation is completed. <br>POC has been presented in a demo.                                                                                                                                                                                                                                                                                                                                               |
| 7.1.6.2        | Deployment Strategy                                                                                                                                                                                                                                                                                                                                  | The provisioning of bundles is carried out independently. <br>There must be an option to selectively activate or deactivate bundles.                                                                                                                                                                                                                                                                                                                                                                             | Configuration is managed via HELM values, allowing flexible adaptation according to the environment.                                                                                                                                                                                                                                                                                                                 |

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
| Product Manager   | Evaluate the dataspace to assess if their product can be used within Catena-X.                       |

## 3.3 System

### 3.3.1 Context Delimitation

#### Existing Umbrella Chart Structure

````mermaid
flowchart
    subgraph "Umbrella Chart"
        ChartYaml["Chart.yaml"]
        subgraph charts
            Portal["Portal"]
            CentralIdp["CentralIdp"]
            SharedIdp["SharedIdp"]
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
    ChartYaml --> SharedIdp
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

# 4 TO-BE Design

## 4.1 People

### 4.1.1 Target Group Analysis

Overall data space roles:

- [Collaboration & Roles](https://catena-x.net/ecosystem/collaboration-roles/)
- [Who: Roles in the Catena-X ecosystem](https://catenax-ev.github.io/docs/operating-model/who-roles-in-the-catena-x-ecosystem)

The relevant data space roles are:

- Data Consumer
- Data Provider
- Enablement Service Provider

#### Scope: Umbrella HELM Charts

- Enablement Services: These services are included under the umbrella of HELM charts, focusing on enabling
  functionalities.

#### Out of Scope:

Core services such as Portal or BPDM are not considered within this scope.

#### Primary target groups:

| No. | Target group                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Data space roles                                                    | Target group differentiation                                                                                                                                                                                                                                                                            | Behaviour, Needs, Pains & Usage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Developers<ul><li>External Developers (not Tractus-X developers): Utilize the chart for demonstration or evaluation purposes.</li><li>Experienced software and product developers who are developing a business app for a CATENA-X data space. They need to develop the app against the interfaces of the data space and integrate them accordingly.</li><li>They emphasize efficient and cost-effective implementation:<ul><li>Cost Efficiency: They do not want to use expensive SaaS solutions.</li><li>Technical Independence: They lack the knowledge and capacity to deploy the enablement and core services of the data space themselves.</li><li>Focus on Development: They concentrate on application development without delving deeply into the deployment and operation of the underlying infrastructure.</li></ul></li><li>Out of Scope: Developers running tests in test runners are not considered within this scope.</li></ul> | Data Consumer <br/> Data Provider <br/> Enablement Service Provider |                                                                                                                                                                                                                                                                                                         | <ul><li>Needs / sources of information<ul><li><a href="https://eclipse-tractusx.github.io/Kits/">Kit documentation tractus-x</a> for interaction purposes</li><li><a href="https://catenax-ev.github.io/">Catena-X documentation</a> for standards and regulations</li><li><a href="https://github.com/eclipse-tractusx/tractus-x-umbrella">Umbrella documentation</a> for umbrella component information</li></ul></li><li>Challenges → Solution<ul><li>Decentralization e.g. Where are other systems? How to interact with them? → Solution: Umbrella charts and bundles for deployment</li><li>Complex setup → Solution: delivery of small capability bundles</li></ul></li></ul> |
| 2   | Tester requiring a test system                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Data Consumer <br/> Data Provider <br/> Enablement Service Provider | <ul><li>Developer (1) tests their feature.</li><li>Tester (2) performs end-to-end testing.</li><li>For the tester, the modular structure is less relevant since they focus on E2E testing, whereas the developer selects the required components.</li><li>The testbed must be easy to deploy.</li></ul> | Same as above from an End-to-end testing perspective.<br/> Typically a tester has less technical know-how than a developer and therefore needs a "one-size-fits-all" (e.g.  Testbed) chart for easier testing.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 3   | SMEs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Data Consumer <br/> Data Provider <br/> Enablement Service Provider |                                                                                                                                                                                                                                                                                                         | Need: SMEs developing a service within the Catena-X Data space want an environment to develop and test their service against without the need for expensive SaaS solutions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## 4.2 Process

### 4.2.1 Use Case View (high-level)

#### Group 1: Product developer

| ID  | Name                                    | Actor             | Description                                                                                                        |
|-----|-----------------------------------------|-------------------|--------------------------------------------------------------------------------------------------------------------|
| UC1 | Configure HELM Chart                    | Product Developer | The product developer configures the HELM Chart for the specific environment.                                      |
| UC2 | Configure Secrets                       | Product Developer | The product developer manages and configures secrets.                                                              |
| UC3 | Execute Deployment Pipeline             | Product Developer | The product developer successfully executes the deployment pipeline for the HELM Chart.                            |
| UC4 | Integrate EDC, DTR, and Identity Wallet | Product Developer | The actors integrate the components EDC, Digital Twin Registry, and Identity Wallet for seamless interoperability. |
| UC5 | Set Up Connection Infrastructure        | Product Developer | The actor sets up the connection infrastructure for linking to the central data space infrastructure.              |
| UC6 | Maintain Infrastructure Module          | Product Developer | The product developer maintains the modular architecture of the HELM Chart.                                        |
| UC7 | Ensure Scalability                      | Product Developer | The product developer ensures scalability to support growing numbers of users and data volumes.                    |
| UC8 | Sandbox Environments                    | Product Developer | The product developer creates local environments to evaluate and experiment with Catena-X components.              |

#### Group 2: Product Tester

| ID  | Name        | Actor          | Description                                                     |
|-----|-------------|----------------|-----------------------------------------------------------------|
| UC9 | E2E Testing | Product Tester | The product tester runs end-to-end tests for Catena-X services. |

#### Group 3: Product Manager

| ID   | Name                 | Actor           | Description                                                                                         |
|------|----------------------|-----------------|-----------------------------------------------------------------------------------------------------|
| UC10 | Dataspace Evaluation | Product Manager | The Product manager evaluates the dataspace to assess if their product can be used within Catena-X. |

#### Use Case diagram

````mermaid
flowchart LR
    PD[Product Developer]
    PT[Product Tester]
    PM[Product Manager]
    UC1[Configure HELM Chart]
    UC2[Configure Secrets]
    UC3[Execute Deployment Pipeline]
    UC4[Integrate EDC, DTR, and Identity Wallet]
    UC5[Set Up Connection Infrastructure]
    UC6[Maintain Infrastructure Module]
    UC7[Ensure Scalability]
    UC8[Sandbox Environments]
    UC9[E2E Testing]
    UC10[Dataspace Evaluation]
    PD --> UC1
    PD --> UC2
    PD --> UC3
    PD --> UC4
    PD --> UC5
    PD --> UC6
    PD --> UC7
    PD --> UC8
    PT --> UC9
    PM --> UC10
````

### 4.2.2 Business Process (SCC Artifact)

#### Chart Release Process

Charts will be released using the already existing workflow in the Umbrella Chart repository. The workflow will
automatically release a Chart, once it is pushed to the "charts/" directory with a new Chart version.

Chart versions should follow [Semantic Versioning](https://semver.org/)

#### Capability Bundle Structure

Capability bundle modularization for the Tractus-X Umbrella Helm chart is a sound architectural and operational design.
It aligns with both the domain-driven architecture of Catena-X (data exchange, digital twin, identity, semantics as
distinct domains) and with Kubernetes best practices for managing complex applications using an umbrella chart to bundle
related microservices.

##### Core Principles

- **Exclusive Assignment**  
  Every component and service is assigned to exactly one capability bundle, ensuring clear ownership and avoiding
  overlap.
- **Separate HELM Sub-Charts**  
  Each bundle is organized as its own Helm sub-chart within the umbrella chart, keeping codebases modular and
  maintainable.
- **Isolated Deployability**  
  Bundles can be deployed in isolation, so failures or updates in one bundle have minimal or no impact on others.
- **Independent Lifecycle Management**  
  Each bundle can be installed, updated, or removed independently, supporting flexible versioning and rollbacks without
  affecting unrelated domains.
- **No Circular Dependencies**  
  Bundles declare only one-way dependencies, ensuring that there are no cycles between bundles.
- **Comprehensive Documentation**  
  The modularization approach—including bundle definitions, dependency rules, deployment instructions, and
  upgrade/removal procedures—is fully documented in the solution concept.

##### Benefits

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

| **Capability Bundle**             | **Default Components**                               | **Comments / Possible Replacements**                                             |
|-----------------------------------|------------------------------------------------------|----------------------------------------------------------------------------------|
| **Identity and Trust bundle**     | - ssi-dim-wallet-stub                                | Can be replaced by your own Identity Wallet.                                     |
| **Dataspace connector bundle**    | - Tractusx connector<br/>- PostgreSQL <br/>- Vault   | Vault can be replaced if you “bring your own” vault or secrets-manager solution. |
| **Digital twin bundle**           | - Digital Twin Registry (DTR)<br/>- PostgreSQL <br/> | DB can be replaced by your own DB solution.                                      |
| **Data persistence layer bundle** | - Simple data backend                                |                                                                                  |

````mermaid
%%{init: {"flowchart": {"subGraphTitleMargin": { "bottom": 10}}}}%%
flowchart LR
    subgraph A["Core Services"]
        Vault["Vault"]
    end

    subgraph B["Capability Bundle: Identity & Trust"]
        SSIWalletStub["SSI Wallet Stub"]
    end

    subgraph C["Capability Bundle: Dataspace Connector"]
        EDC["EDC"]
        EDCDB["EDC DB"]
        EDC .-> EDCDB
    end

    subgraph "Capability Bundle: Digital Twin"
        DTR["DTR"]
        DTRDB["DTR DB"]
        DTR .-> DTRDB
    end

    subgraph "Capability Bundle: Data Persistence Layer"
        SimpleSubmodelServer["Simple Submodel Server"]
    end

    subgraph "Hausanschluss Actors"
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

    EDC -..-> SSIWalletStub
    EDC -..-> Vault
    DataProvider --> EDC
    DataProvider --> DTR
    DataProvider --> SimpleSubmodelServer
    DataConsumer --> EDC
    EnablementProvider --> DataConsumer
    EnablementProvider --> DataProvider
````

#### Deployment strategies

##### Role: Data Provider

The standard data provider role consists of an EDC, DTR and Submodel Server Bundles. EDC uses the Identity Wallet
Bundle.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Data Persistence Layer"]
    C["Capability Bundle: Dataspace Connector"]
    D["Capability Bundle: Digital Twin"]
    E("Application to be tested/developed")
    style E fill: #afafaf, color: black
    F{{"Developer/Tester"}}
    E --> B
    E --> C
    E --> D
    C --> A
    F --> E
````

##### Role: Data Consumer

The standard data consumer role consists of only the EDC Bundle and the Identity Wallet Bundle.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Dataspace Connector"]
    C("Application to be tested/developed")
    style C fill: #afafaf, color: black
    D{{"Developer/Tester"}}
    C --> B
    B --> A
    D --> C
````

##### Role: Enablement Provider

The Enablement Provider role consists of both the Data Consumer and Data Provider bundles. This allows provisioning of
data and the consumption of the provisioned data by a application.

````mermaid
flowchart BT
    A["Capability Bundle: Identity & Trust"]
    B["Capability Bundle: Data Persistence Layer"]
    C("Application to be tested/developed")
    style C fill: #afafaf, color: black
    D["Capability Bundle: Digital Twin"]
    E["Capability Bundle: Dataspace Connector (Provider)"]
    F["Capability Bundle: Dataspace Connector (Consumer)"]
    G{{"Developer/Tester"}}
    C --> B
    C --> D
    C --> E
    C --> F
    E --> A
    F --> A
    G --> C
````

#### Bring your own

Each Bundle can be deactivated to use your own component. This requires configuration of the component specific
parameters in the other components.

In this example this would be the configuration of the Identity Wallet within the EDC.

````mermaid
flowchart BT
    A("Application to be tested/developed")
    style A fill: #afafaf, color: black
    B["Capability Bundle: Dataspace Connector"]
    C["<s>Capability Bundle: Identity & Trust</s>"]
    D["Own Identity Wallet"]
    E{{"Developer/Tester"}}
    A --> B
    B -- identitywallet - bundle . enabled = false --> C
    B -- configure --> D
    E --> A
````

Using a "bring-your-own" component requires additional configuration. In this case, the identity wallet has to be
configured in the EDC configuration section.

Replacing existing Charts with your own solution is not limited to the direct components of the Capability Bundles.  
This also applies to the dependencies of the bundles which e.g. allows the user to choose another way of provisioning a
database.

Components which can be replaced are:

- Capability Bundle: Dataspace Connector
    - postgresql
    - vault
- Capability Bundle: Digital Twin
    - postgresql
    - keycloak
- Capability Bundle: Identity & Trust
    - ssi-dim-wallet-stub
- Capability Bundle: Data Persistence Layer
    - simple-data-backend

To make configuration of "bring-your-own" components easier, the bundle config has to highlight which values are
related to which dependency and what to change, if the components should be replaced:

```yaml
digital-twin-registry:
  registry:
    dataSource:
    # replace this when using your own database
    # url: 
    # user: 
    # password: 
```

#### Scalability

It is essential that the deployment of each bundle is entirely independent, allowing the same bundle to be deployed
multiple times.  
Every instance must maintain its own unique set of Kubernetes resources, ensuring there is no overlap or shared
dependencies between different deployments.

#### Interoperability

To ensure interoperability, the [Tractus-X Release Guidelines](https://eclipse-tractusx.github.io/docs/release/) are
followed and [Catena-X standards](https://catenax-ev.github.io/docs/standards/overview) are understood and applied.  
Additionally, the existing functionality of the Umbrella Chart must be kept and verified to work.

### 4.2.2.1 Reduction of Complexity in the Deployment Process

#### 1. Standardization of Bundle Configuration

**Goal: Make "Bring-Your-Own" components easier to configure**

Each chart should provide clear default values for all optional components (e.g. `postgresql.enabled=false`,
`external.postgresql.url=...`).

Clearly mark all BYO-related config sections in values.yaml, like:

```yaml
# === Bring Your Own ===
postgresql:
  enabled: false
  external:
    host: my-own-db
    port: 5432
````

**Out of scope:**

Usage of central _helpers.tpl functions to standardize naming conventions across all charts. _(Helper functions can not
be used as templates of 3rd party HELM charts can not be modified or extended)_

#### 2. Automated Validation & Linting in CI

**Goal: Increase robustness & transparency**

Extend umbrella chart workflow with:

* helm lint on subcharts and umbrella chart
* automated ci tests with minimal configuration

Example (GitHub Action or GitLab CI):

```yaml
- run: ct lint --charts charts/my-bundle
- run: ct install --charts charts/my-bundle
````

#### 3. Reduction of configuration steps

**Goal: Simplify deployment by minimizing manual configuration.**

The Helm Charts provided for the components in the Capability Bundles offer extensive configuration options, which can
be overwhelming when deploying for test or development purposes. By applying a pre-configuration that omits default
values, the Bundles streamline their values.yaml files to display only the essential properties that require attention.

This approach not only enhances the readability of the configuration but also clearly indicates what needs to be set.
Supplementary documentation further clarifies the necessary configuration options and their corresponding values.

#### 4. CLI or Script Support for Custom Deployments

**Goal: Improve usability & reduce user error**

Create a simple CLI tool (e.g., Bash, Python, Go) that:

* Loads environment variables
* Generates values.yaml files from templates
* Triggers the Helm deployment

**Warning:** technical feasibility needs to be evaluated

#### 5. Dynamic Naming for Multiple Deployments

**Goal: Enable scalability**

Use the chart installation name as prefix when the chart allows templating of values:

```yaml
name: {{ .Release.Name }}-edc
```

This allows deploying multiple instances of the same bundle in one cluster:

```bash
helm install edc-a .
helm install edc-b .
```

**Warning:** This is only possible if the Helm Chart supports templating for the specific property.

#### 6. Documentation & Visibility

**Goal: Transparency for users**

Structured README per bundle:

* What is optional?
* What must be configured?
* How to replace a component with BYO?
* Include tables listing supported overrides (Markdown or auto-generated)

## 4.3 System

### 4.3.1 Context Delimitation / 4.3.2 Interface Documentation

Interactions between an Application acting as Dataprovider or Dataconsumer and the Services which are part of the
different Capability Bundles.

````mermaid
flowchart LR
    Dataprovider["Dataprovider"] -->|stores data| SubmodelServer["Submodel Server"]
    Dataprovider -->|creates twins| DTR["DTR"]
    Dataprovider -->|creates contracts| EDC["EDC"]
    EDC["EDC"] -->|needs| EdcPosgtres["PostgreSQL Database"]
    Dataconsumer["Dataconsumer"] -->|negotiate contracts| EDC
    DTR -->|needs| DtrPostgres["PostgreSQL Database"]
    EDC["EDC"] -->|needs| IdentityWallet["Identity Wallet"]
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

- **Chart-testing Tool**: Validation of the Helm Charts based on Kubernetes schemas.
- **Local Cluster Tests**: Use of tools such as Kind or Minikube to perform integration tests in a test environment.

##### Release Management & Deployment

- **Chart Releaser**: Automated creation and publication of chart releases.
- **Helm Chart Repository / GitHub Packages**: Hosting and provisioning of the finalized charts.

# NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
