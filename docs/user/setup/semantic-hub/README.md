# Semantic Hub Setup

This guide provides instructions to configure and enable the Semantic Hub component.

## Precondition: Build the Fuseki Docker Image

The Semantic Hub requires a compatible Fuseki Docker image. Follow these steps to build the image:

1. **Download the Fuseki Docker Files**:
   Download the `jena-fuseki-docker-5.0.0.zip` file from the Maven repository:
   [Download Fuseki Docker](https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-docker/5.0.0/jena-fuseki-docker-5.0.0.zip).

2. **Extract the Zip File**:
   ```bash
   unzip jena-fuseki-docker-5.0.0.zip
   cd jena-fuseki-docker-5.0.0
   ```

3. **Build the Docker Image**:
   ```bash
   docker build --build-arg JENA_VERSION=5.0.0 -t jena-fuseki-docker:5.0.0 --platform linux/amd64 .
   ```

## Enabling Semantic Hub

Once the Fuseki Docker image is built and available, enable the Semantic Hub in the Helm values file.

1. Update the `values.yaml` file to enable the `semantic-hub` component:
   ```yaml
   semantic-hub:
     enabled: true
   ```

2. Deploy the Umbrella Chart with the updated configuration:
   ```bash
   helm upgrade --install umbrella . --namespace umbrella --create-namespace
   ```

## Accessing the Semantic Hub

Once deployed, the Semantic Hub will be accessible at the following endpoint:
```bash
http://semantics.tx.test/discoveryfinder/swagger-ui/index.html
```

## Notes

- Ensure that the `semantic-hub` component is running by checking the Kubernetes pods:
  ```bash
  kubectl get pods --namespace umbrella
  ```

- Use the Swagger UI to interact with the Semantic Hub's API for testing and integration.

For further details, refer to the [official documentation](https://jena.apache.org/documentation/fuseki2/).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
