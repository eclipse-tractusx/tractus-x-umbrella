# Semantic Hub Setup

Required only if you enable `semantic-hub` in your values file. The Semantic Hub
needs a compatible Fuseki Docker image that must be built locally (it is not
published to any public registry).

## 1. Build the Fuseki image

```bash
# Download the Fuseki Docker files
curl -L -o jena-fuseki-docker-5.0.0.zip \
  https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-docker/5.0.0/jena-fuseki-docker-5.0.0.zip

unzip jena-fuseki-docker-5.0.0.zip
cd jena-fuseki-docker-5.0.0

docker build --build-arg JENA_VERSION=5.0.0 \
  -t jena-fuseki-docker:5.0.0 \
  --platform linux/amd64 .
```

> On Minikube, load the image into the cluster's docker daemon:
> `eval $(minikube docker-env)` before building, or use `minikube image load`.

## 2. Enable Semantic Hub

In your values file:

```yaml
semantic-hub:
  enabled: true
```

Deploy or upgrade:

```bash
helm upgrade --install umbrella charts/umbrella \
  --namespace umbrella --create-namespace
```

## 3. Access

```
http://semantics.tx.test/discoveryfinder/swagger-ui/index.html
```

Check the pod is running:

```bash
kubectl get pods --namespace umbrella -l app.kubernetes.io/name=semantic-hub
```

For more on Fuseki: <https://jena.apache.org/documentation/fuseki2/>.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
