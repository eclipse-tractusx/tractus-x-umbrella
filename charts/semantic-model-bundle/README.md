# Semantic Model Bundle

The Semantic Model Bundle provides semantic modeling and submodel management capabilities for the Catena-X ecosystem. It includes the Submodel Mock and Semantic Hub services.

## Components

- **Submodel Mock**: Simulates submodel functionality for testing and development
- **Semantic Hub**: Manages semantic models and their relationships
- **Semantic Model Registry**: Stores and manages semantic model definitions

## Prerequisites

- Kubernetes cluster (version 1.24 or higher)
- Helm (version 3.8 or higher)
- kubectl configured to access your cluster

## Installation

### Standalone Installation

To install the Semantic Model Bundle standalone:

```bash
# Add the repository
helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev

# Install the bundle
helm install semantic-model-bundle ./charts/semantic-model-bundle
```

### Installation with Umbrella Chart

To install as part of the umbrella chart:

```bash
helm install umbrella ./charts/umbrella --set semantic-model-bundle.enabled=true
```

## Configuration

The bundle can be configured through the `values.yaml` file or using `--set` flags. Key configuration options include:

### Submodel Mock Configuration

```yaml
submodel-mock:
  enabled: true
  image:
    repository: eclipse-tractusx/submodel-mock
    tag: "0.4.0"
  service:
    type: ClusterIP
    port: 8080
```

### Semantic Hub Configuration

```yaml
semantic-hub:
  enabled: true
  config:
    hub:
      api:
        baseUrl: "http://semantic-hub:8080"
      persistence:
        enabled: true
        type: "memory"
```

## Usage

### Accessing the Submodel Mock

After installation, the Submodel Mock API will be available at:
```
http://<service-name>:8080
```

### Using the Semantic Hub

1. Access the Semantic Hub API:
   ```
   http://<semantic-hub-service>:8080
   ```

2. Register a semantic model:
   ```bash
   curl -X POST http://<semantic-hub-service>:8080/api/v1/models \
     -H "Content-Type: application/json" \
     -d '{
       "id": "urn:model:example",
       "version": "1.0.0",
       "name": "Example Model",
       "description": "An example semantic model"
     }'
   ```

## Security

The bundle includes security features:
- OAuth2 authentication
- Role-based access control
- Secure model storage and retrieval

## Troubleshooting

Common issues and solutions:

1. **Submodel Access Issues**
   - Check submodel service status: `kubectl get svc -l app.kubernetes.io/name=submodel-mock`
   - Verify authentication configuration

2. **Semantic Hub Issues**
   - Check hub service logs: `kubectl logs -l app.kubernetes.io/name=semantic-hub`
   - Verify model persistence configuration

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 