# 1. Business Case

The Tractus-X Umbrella Helm Chart is a foundational deployment tool for Catena-X infrastructure. To meet TRL 7 maturity, it must support fully automated, cloud-native deployment, secure secrets management, and GitOps workflows. This solution concept enables deployment across cloud environments (INT and STABLE) and integrates critical components like Vault, ArgoCD, and a BYO Clearing House.

# 2. Requirements Analysis

## 2.1 Premises

- Kubernetes clusters (INT and STABLE) are provided and maintained by CATENA-X e.V.
- Networking and ingress via NGINX are already configured.
- ArgoCD is installed and preconfigured; no customizations will be made.
- Vault is available and configure in ArgoCD
- Access to external systems Clearing House and Wallet (?) is available
  - ℹ️ alternative is to mock the components
- Only Enablement and Core Services are in scope.

## 2.2 Requirements Catalog

### **Solution Concept for Umbrella HELM Charts**

- Analysis and evaluation of the existing Umbrella HELM Charts with respect to their suitability for deployment in a cloud infrastructure.
- Identification and description of necessary adjustments to the HELM Charts, considering configuration, architectural, and cloud-specific requirements.
- Examination of security-relevant aspects such as secrets management and development of optimization proposals.
- Analysis of limitations that hinder or prevent deployment in test environments and TRL 7 cloud environments.
- Development of an implementation concept with actionable recommendations for cloud optimization of the Umbrella HELM Charts.

### **Deployment of the Umbrella HELM Charts on Kubernetes**

- Deployment of the Umbrella HELM Charts to a provided Kubernetes environment in a cloud setting.
- Integration with an existing **HashiCorp Vault** system for secrets management.
- Integration into an existing, pre-configured **ArgoCD** setup for continuous delivery.
- Support for **BYO (Bring Your Own)** Clearing House integration.
  - Integration with an existing **ArgoCD**
  - Connection to a **Vault system** for secrets
  - **BYO Clearing House** integration
  - Creation of a **documented, repeatable installation** process

### **Deployment of a HashiCorp Vault**

- Implementation of the deployment of a HashiCorp Vault.
- Setup and configuration of the Vault for operation in both INT and STABLE environments.
- Integration of the Vault into the existing Umbrella HELM Chart.
- Documentation of the deployment and integration for operations and further development.
- Execution of a **knowledge transfer** for working with Vault.
- Ensuring the use of Vault secrets within the defined components.
- Secure secrets management for **Tractus-X components** in Kubernetes
- Setup of a Vault instance for INT and STABLE environments
- Integration with the Umbrella HELM Chart
- Configuration of **product-specific namespaces**
- Creation of **deployment and operations documentation**

### **TLS Encryption Within the Cluster**

- Implementation of a suitable architecture for TLS-encrypted communication within the cluster.
- Selection and deployment of a certificate authority within the existing Kubernetes environment.
- Configuration for the automatic issuance, renewal, and management of TLS certificates for cluster services.
- Configuration of Ingress controllers and services to use TLS certificates.
- Definition of certificate policies (e.g., validity periods, renewal intervals).
- Documentation of installation, configuration, and operational processes.

# 3. Current Situation

## 3.1 Process

### 3.1.1 Use Case View

- Local Helm-based deployments using hardcoded values.
- TLS and Vault are not yet integrated.

### 3.1.2 Business Process View

- Developers manually deploy Umbrella Chart to local clusters.
- Configurations are maintained in static files.

## 3.2 Configuration & Secrets

### 3.2.1 Helm Values

- Lacks environment-specific profiles.
- Hardcoded secrets not suitable for cloud environments.

### 3.2.2 Secrets Management

- No Vault support in the existing umbrella chart
- Secrets stored plain in values.yaml

### 3.2.3 Security

- TLS not enforced internally.
- Secrets exposed in plaintext.

## 3.3 System

### 3.3.1 Context Delimitation

- Components deployed via Helm in one namespace.
- Vault and Clearing House are mocked.

### 3.3.2 Interfaces

- Lokal Kubernetes Cluster

## 3.4 Decision on Solution

### 3.4.1 Decision Matrix for Solution Alternatives

#### Example (not actual options):

| Feature        | Option A: Native K8s Secrets | Option B: Vault Integration |
|----------------|------------------------------|-----------------------------|
| Security       | ❌ Low                        | ✅ High                      |
| Flexibility    | ❌ Hardcoded                  | ✅ Dynamic                   |
| Automation     | ❌ Manual                     | ✅ Automated                 |
| Recommendation | ❌                            | ✅ Use Vault                 |

# 4. Future Design

## 4.1 Process

### 4.1.1 Target Use Case

- Deploy via ArgoCD to a kubernetes cluster (env to be determined)
- Vault manages secrets securely (?) or other secret management
- TLS via cert-manager and internal CA.
- Fully documented, repeatable process.

## 4.2 Configuration & Secrets

### 4.2.1 Configuration

- Environment-specific values files (?) TBD which env
- Global vs. component-level settings

### 4.2.2 Vault Template Strategy

TBD

### 4.2.3 TLS Policies

- Internal CA via cert-manager.
- Automatic renewal.
- No external CA or app-level changes.

## 4.3 System

### 4.3.1 Helm Chart Architecture

- Selective enablement for BYO integrations (Clearing House, Wallet)
- Reusable base values and overrides

### 4.3.2 Interfaces

- Helm, ArgoCD, Vault, cert-manager.

### 4.3.3 Security Model

- TLS on ingresses.
- Vault for secrets.

### 4.3.4 Namespace Strategy

- Shared namespace with RBAC and isolation.
- One Vault mount path per environment.

# 5. Build

## 5.1 Tooling

- Helm
- ArgoCD (preconfigured)
- cert-manager (internal CA)
- Vault (preconfigured)
- Kubernetes
- GitHub Actions

# 6. Quality Assurance

## 6.1 Process

- Helm linting and validation.
- Ephemeral testing via Kind or Minikube.
- No formal test management process in scope.

## 6.2 Testing

How can we test the functionality?
Is test automation possible?
Do we need automated tests?

- Deployment validation
- Secret injection checks (?)
- TLS verification

### 6.2.2 Test Levels

- Unit: Template rendering
- Integration: Chart + Vault + ArgoCD (?)
- E2E: Deploy the entire stack to INT

## 8. Documentation & Compliance

### 8.1 Open Source Compliance

- SPDX headers in all source files
- Apache 2.0 license for Code included
- CC-BY-4.0 license for non-Code included

### 8.2 Documentation Assets

- Architecture Decision Records (ADRs)
- API documentation (OpenAPI, JSON schema)
- Testing and release documentation

# 7. Project Management

## 7.1 Stakeholder Analysis

- Infra (Vault, ArgoCD): CATENA-X e.V.
- Chart Owners: Umbrella maintainers
- Lead: Felix Gerbig
- Umbrella Lead: Evelyn Gurschler

## 7.2 Open Items List and Decision Log

- Secret integration strategy
- Clearing House configuration
- Helm jobs
- ArgoCD Vault compatibility

## 7.3 Risk List
