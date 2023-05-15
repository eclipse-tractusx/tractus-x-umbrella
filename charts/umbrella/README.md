# E2E umbrella Chart

This e2e umbrella Chart is a basis for end-to-end testing of an [Catena-X](https://catena-x.net/en/) automotive dataspace network
consisting of [Tractus-X](https://projects.eclipse.org/projects/automotive.tractusx) OSS coponents.

The Chart aims for a completely automated setup of a fully functional network, that does not require manual setup steps.

## Installing

Running this Chart requires a kubernetes cluster `>1.24.x`. One of the options is to run a local instance of [minikube](https://minikube.sigs.k8s.io/docs/start/) setup.
Assuming you have a running cluster and your `kubectl` context is set to that cluster, you can use the following command to install
the Chart as `lab` release.

```shell
# Download (recursive chart dependencies) with hack script
hack/helm-dependencies.bash

cd charts/umbrella

helm install lab . --namespace lab --create-namespace
```

To taredown your setup, run:

```shell
helm delete lab --namespace lab
```

## How to contribute

Before contributing, make sure, you read and understood our [contributing guidelines](./CONTRIBUTING.md).
We appreciate every contribution, be it bug reports, feature requests, test automation or enhancements to the Chart(s),
but please keep the following in mind:

- Avoid company specific setup
- Avoid any tooling/infra components, that requires a subscription in any form
- Be vendor and cloud agnostic
