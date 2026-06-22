# Umbrella Helm

## Goals

> - It shall be ready for the next Tractus-X Community Event!
> - At the end of the consortia: To have one deployable result of the whole dataspace.
> - Setting up an complete environment for e2e testing purpose.
> - Including seeding data to let the automated tests run
> - Only FOSS Applications will be part of this chart
> - It shall be highly configurable

## Plan

Complete list of content of the umbrella helm chart

1. Shared Services
   1. :white_check_mark: Portal incl. IDP
   2. :white_check_mark: Discovery Services
   3. Semantic Hub (to be prepared)
   4. GDPM 
      (Product Ticket: https://github.com/eclipse-tractusx/bpdm/issues/738 )
      (Issue: https://github.com/eclipse-tractusx/bpdm/issues/795)
   5. :white_check_mark: SD-Factory
   6. :white_check_mark: MIW & Vault (PR: https://github.com/eclipse-tractusx/tractus-x-umbrella/pull/57)
2. :white_check_mark: Industry Core (Ready for integration --> https://github.com/eclipse-tractusx/tractus-x-umbrella/pull/53)
   1. :white_check_mark: Data Provider 1
      1. EDC
      2. Submodel Server
      3. Registry
      4. :white_check_mark: Simple Data Backend
   2. :white_check_mark: Data Provider 2
   3. :white_check_mark: Data Provider 3
3. Business Applications
   1. Trace-X A
   2. Trace-X B

> [!IMPORTANT]  
> MIW vs. SD-Factory \
> HashiCorp VAULT

## Seeding Data

List of data necessary data objects

* Trace-X Testdata
  * asBuilt test data
  * asPlanned test data
  * BPN's (Testdatafile)
  * user credentials
  * technical credentials
  * url's to shared services

> [!IMPORTANT]  
> Add Links

You will find a list of all seeds necessary for this helm chart within the files seeds_** 

## Contributions

IRS Team:

* Development ressources to build Umbrella helm
* Workshop for initial setup of Umbrella Helm
* Business steering to bring parties together

Arena2036:

* Development ressources to build Umbrella helm

Portal:

* Development ressources to build Umbrella helm

System Team:

* Development ressources to build Umbrella helm

EDC:

* **under discussion**

Assosiation:

* possible expert group to take over responsibility after consortia ends in Jul 24

@stephanbcbauer:

* development contributions

## Key Features of Umbrella Helm

1. Deploys the necessary Applications on which the dataspace runs
2. It is configurable, what services/applications/data shall be deployed
3. It contains testdata which is seeded into the different layers of this deployment
4. It can be used to be installed by anyone on local machines
5. It is the base for automatic E2E Testing.

## Folder Structure

```text
.🗂 charts                             -> 
  ├──🗂 umbrella                       -> umbrella chart for configuration of setup  
    ├──🗂 templates
    ├──🗂 seedingData                  -> folder to structure seeding data
      ├──🗂 sharedServices
      ├──🗂 industryCore 
      ├──🗂 businessApplications 
```

## Open Topics

* [x] Is it possible to use arbitrary BPN's which are being seeded?
* [x] Do we need a new set of BPN values for that case? --> No lets use the existing of the test data files
* [x] Which version of the test data shall be used? --> 1.6.5?
* [x] Which technology stack is to be used for this? Helm or Terraform? --> HELM
  * [x] How does it fit to the Tutorial? --> It does not fit yet. Multiple Ideas exist. transfer the tutorial from terraform to Helm.
* [x] Shall we use Helm test to check if services are online within the deployment phase? --> Yes use init setup or hooks.
* [x] Which Helm version are we using? --> Helm 3
* [x] How are we seeding Data? --> post-install, post-upgrade hook's
* [x] with which release shall be started? --> stable 23.12 <https://github.com/catenax-ng/catena-x-release-deployment/tree/main/stable/23.12>
* [ ] take over naming conventions from the tutorial as much as possible?

### TODO's

* [x] draft Portal seeding data @jzbmw @Evelyn --> 25.01
* [x] invite @tunahan Discovery Services and Semantic Hub @jzbmw @Gabor @tunahan @Evelyn -->
  * Semantic Hub time necessary to build the Helm Chart
  * Charts for Discovery finders will be added to shared Services
* [x] cleanup of Repo -> @Gabor --> 29.01
* [x] BPN selection for IDP
* [x] Helm Test Timout investigation/ Bigger Github Runner @Gabor
* [x] @Evelyn: Check for Helm Test in Helm Chart --> leads to timeout during deployment
* [x] @Jaro: Status Data Provider --> currently ongoing. First Helm chart exists. Challanges with namespaces of using same chart 3 times with namespaces, for example databases
* [x] @Jaro: Build a SubmodelServer--> used the existing one of IRS Team
* [x] @Jaro: dDTR Version ( support from @Tuna )
* [x] @Tuna: Discovery Service Helm PR
* [x] @Johannes: BPDM Status <https://github.com/eclipse-tractusx/bpdm/issues/738>
* [x] @Johannes: SD-Factory --> https://github.com/eclipse-tractusx/sd-factory/issues/91
* [x] Awareness to Open Planning regarding E2E vs. tutorials
* [x] setup Helm/Folder structure
  * [x] Define Helm setup
  * [x] Define Helm how to seed data --> f.e. <https://helm.sh/docs/topics/charts_hooks/> vs. <https://stackoverflow.com/questions/71284091/helm-run-pods-and-dependencies-with-a-predefined-flow-order> vs. <https://itnext.io/database-migrations-on-kubernetes-using-helm-hooks-fb80c0d97805>
* [x] collect Seeding/Test data
  * [x] BPN's
  * [x] Trace-X Testdata
  * [x] Current Testdatafile

* [ ] Documentation (e.g. OpenApi / Swagger, Insomnia Collection, Tutorials-> E2E Documentation, Step-By-Step Guide)
* [ ] @Evelyn: Setup new Environment for definition of Companies -> conducting when the components are integrated
* [x] @Jaro & @Evelyn: Have a look on the MIW Helm Chart
* [x] @Jaro: EDC Chat to clarify on secrets via configuration to reduce the Vault as ressource
* [ ] @Garbor: Update of TRG's 5.0.5 -> see also https://github.com/eclipse-tractusx/eclipse-tractusx.github.io/pull/755
* [x] @Johannes: Status BusinessApps Helm Chart
* [ ] @All: Ingress discussions & Testing configuration
* [ ] @All: TLS Setup
* [ ] Tractus-X Community Days
* [ ] @All: update components to 24.03 Release
* [ ] Semantic Hub integration ongoing, some issues remain, Tuna is investigating them. Update will be in the EF Matrix chat as he'll be gone for a month. https://github.com/eclipse-tractusx/tractus-x-umbrella/pull/61

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

