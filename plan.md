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

* [ ] setup Helm/Folder structure
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

* Is it possible to use arbitrary BPN's which are being seeded?
* Do we need a new set of BPN values for that case? --> No lets use the existing of the test data files
* Which version of the test data shall be used? --> 1.6.5?
* Which technology stack is to be used for this? Helm or Terraform? --> HELM
  * How does it fit to the Tutorial? --> It does not fit yet. Multiple Ideas exist. Transfer Tutorial in Helm.

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

* **under discussion**

EDC:

* **under discussion**

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
    ├──🗂 charts                       -> 
    ├──🗂 templates                    ->
    ├──🗂 seedingData                  -> folder to structure seeding data
```
