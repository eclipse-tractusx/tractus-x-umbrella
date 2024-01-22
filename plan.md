# Umbrella Helm

This umbrella helm chart is for the following purposes and requirements:

* Setting up an complete environment for e2e testing purposes
* Including seeding data to let the automated tests run
* Only FOSS Applications will be part of this chart
* It shall be highly configurable

## Plan

Complete list of content of the umbrella helm chart

1. Shared Services
   1. Portal incl. IDP
   2. MIW
   3. Discovery Services
   4. Semantic Hub
   5. GDPM
2. Industry Core
   1. Data Provider 1
      1. EDC
      2. Submodel Server
      3. Registry
   2. Data Provider 2
   3. Data Provider 3
3. Business Applications
   1. Trace-X A
   2. Trace-X B

* [x] draft Portal seeding data @jzbmw @Evelyn --> 25.01
* [x] invite @tunahan Discovery Services and Semantic Hub @jzbmw @Gabor @tunahan @Evelyn --> 
  * Semantic Hub time necessary to build the Helm Chart
  * Charts for Discovery finders will be added to shared Services
* [ ] cleanup of Repo -> @Gabor --> 29.01
* [ ] Awareness to Open Planning regarding E2E vs. tutorials
* [ ] setup Helm/Folder structure
  * [ ] Define Helm setup
  * [ ] Define Helm how to seed data --> f.e. https://helm.sh/docs/topics/charts_hooks/ vs. https://stackoverflow.com/questions/71284091/helm-run-pods-and-dependencies-with-a-predefined-flow-order vs. https://itnext.io/database-migrations-on-kubernetes-using-helm-hooks-fb80c0d97805
* [ ] collect Seeding/Test data
* [ ] implement Shared Services Helm
* [ ] implement Mechanism to provision Seeding data
* [ ] implement Shared Services seeding data
* [ ] run first minimal Helm setup
* [ ] implement Script to split test data
* [ ] implement the Data Providers Helm
* [ ] implement Data Provider Helm seeding data
* [ ] implement Business App Helm
* [ ] implement Business App seeding data

## Goal

> It shall be ready for the next Tractus-X Community Event!
> At the end of the consortia: To have one deployable result of the whole dataspace.

## Seeding Data

List of data necessary data objects

* Trace-X Testdata
  * asBuilt test data
  * asPlanned test data
  * BPN's (Testdatafile)
  * user credentials
  * technical credentials
  * url's to shared services

## Open Topics

* [ ] Is it possible to use arbitrary BPN's which are being seeded?
* [x] Do we need a new set of BPN values for that case? --> No lets use the existing of the test data files
* [x] Which version of the test data shall be used? --> 1.6.5?
* [x] Which technology stack is to be used for this? Helm or Terraform? --> HELM
  * [x] How does it fit to the Tutorial? --> It does not fit yet. Multiple Ideas exist. transfer the tutorial from terraform to Helm.
* [ ] Shall we use Helm test to check if services are online within the deployment phase?
* [x] Which Helm version are we using? --> Helm 3
* [x] How are we seeding Data? --> post-install, post-upgrade hook's
* [x] with which release shall be started? --> stable 23.12 https://github.com/catenax-ng/catena-x-release-deployment/tree/main/stable/23.12
* [ ] take over naming conventions from the tutorial as much as possible?

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
      ├──🗂 sharedServices
      ├──🗂 industryCore
      ├──🗂 businessApplications 
    ├──🗂 templates
    ├──🗂 seedingData                  -> folder to structure seeding data
      ├──🗂 sharedServices
      ├──🗂 industryCore 
      ├──🗂 businessApplications 
```
