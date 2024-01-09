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
2. Minimal Data Space (Industry Core)
   1. Data Provider 1
      1. EDC
      2. Submodel Server
      3. Registry
   2. Data Provider 2
   3. Data Provider 3
3. Business Applications
   1. Trace-X A
   2. Trace-X B

## Seeding Data

List of data necessary data objects

* Trace-X Testdata
  * asBuilt test data
  * asPlanned test data
  * BPN's
  * user credentials
  * technical credentials
  * url's to shared services

## Open Topics

* Is it possible to use arbitrary BPN's which are being seeded?
* Do we need a new set of BPN values for that case?
* Which version of the test data shall be used? --> 1.6.5?
* Which technology stack is to be used for this? Helm or Terraform?
