# Tutorial: API Requests for Data Exchange

This tutorial explains how to configure Bruno and retrieve the correct `API_KEY` before executing the Data Exchange API requests.

The guide covers the additional steps that are required to successfully authenticate requests against the IssuerService after deploying the Umbrella Chart.

## Prerequisites

Before executing the API requests, ensure that:

- The Umbrella Chart has been successfully deployed.
- All required pods are in the `Running` state.
- `kubectl` is installed and configured to access the cluster.
- **Bruno** is installed.

Download Bruno from the official website:

https://www.usebruno.com/downloads

## Deploy the Umbrella Chart

Deploy the Umbrella Chart following the existing deployment documentation.

Once the deployment has finished, verify that all required pods are running:

```bash
kubectl get pods
```

Example output:

```text
umbrella-issuerservice-xxxxx        Running
umbrella-dataconsumer-xxxxx         Running
umbrella-dataprovider-xxxxx         Running
...
```

## Retrieve the API_KEY

The `API_KEY` used by the IssuerService is generated dynamically and may change after every deployment.

If an outdated key is used, authentication requests from Bruno will fail.

First, locate the IssuerService pod:

```bash
kubectl get pods
```

Then display its logs:

```bash
kubectl logs pod/umbrella-issuerservice-<pod-name>
```

Locate the generated `API_KEY` in the logs.

## Configure Bruno

Open the appropriate Bruno collection for your deployment profile.

Update the `API_KEY` environment variable with the value obtained from the IssuerService logs.

Save the environment before executing any requests.

## Execute the Requests

Once Bruno has been configured:

- Open the appropriate Data Exchange collection.
- Execute the requests in the documented order.
- Verify that authentication succeeds and the requests complete successfully.

## Troubleshooting

### Authentication fails

If Bruno returns authentication errors (for example `401 Unauthorized` or `403 Forbidden`):

- Verify that the configured `API_KEY` is up to date.
- Retrieve the latest key from the IssuerService logs:

```bash
kubectl logs pod/umbrella-issuerservice-<pod-name>
```

- Update the `API_KEY` environment variable in Bruno.
- Retry the request.

### Bruno is not installed

Bruno is required to execute the provided `.bru` collections.

Download the latest version from:

https://www.usebruno.com/downloads

## Expected Result

After completing this tutorial:

- Bruno is installed.
- The Umbrella Chart is running successfully.
- The current `API_KEY` has been retrieved from the IssuerService logs.
- Bruno has been configured with the correct environment variables.
- The Data Exchange API requests execute successfully.

## NOTICE

This work is licensed under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

* SPDX-License-Identifier: Apache-2.0
* SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
* SPDX-FileCopyrightText: 2026 LKS Next
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>