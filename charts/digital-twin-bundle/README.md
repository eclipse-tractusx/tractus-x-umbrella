# Digital Twin Bundle

The Digital Twin Bundle provides a complete solution for managing digital twins in the Catena-X ecosystem. It includes the Decentral DT Registry and its required dependencies.

## Components

- **Decentral DT Registry**: The core component for managing digital twin registrations and metadata
- **PostgreSQL**: Database for persistent storage of digital twin data
- **Digital Twin API**: REST API for interacting with digital twins

## Prerequisites

- Kubernetes cluster (version 1.24 or higher)
- Helm (version 3.8 or higher)
- kubectl configured to access your cluster

## Installation

### Standalone Installation

To install the Digital Twin Bundle standalone:

```bash
# Add the repository
helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev

# Install the bundle
helm install digital-twin-bundle ./charts/digital-twin-bundle
```

### Installation with Umbrella Chart

To install as part of the umbrella chart:

```bash
helm install umbrella ./charts/umbrella --set digital-twin-bundle.enabled=true
```

## Configuration

The bundle can be configured through the `values.yaml` file or using `--set` flags. Key configuration options include:

### DT Registry Configuration

```yaml
dt-registry:
  enabled: true
  image:
    repository: eclipse-tractusx/dt-registry
    tag: "0.4.0"
  service:
    type: ClusterIP
    port: 8080
```

### PostgreSQL Configuration

```yaml
postgresql:
  enabled: true
  auth:
    username: dt
    password: dt
  primary:
    persistence:
      size: 10Gi
```

## Usage

### Accessing the DT Registry

After installation, the DT Registry API will be available at:
```
http://<service-name>:8080
```

### API Documentation

The DT Registry API documentation is available at:
```
http://<service-name>:8080/swagger-ui.html
```

## Security

The bundle includes security features:
- OAuth2 authentication
- Role-based access control
- Secure communication with other services

## Troubleshooting

Common issues and solutions:

1. **Database Connection Issues**
   - Check PostgreSQL pod status: `kubectl get pods -l app.kubernetes.io/name=postgresql`
   - Verify database credentials in the configuration

2. **API Access Issues**
   - Check service status: `kubectl get svc -l app.kubernetes.io/name=dt-registry`
   - Verify network policies and ingress configurations

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 