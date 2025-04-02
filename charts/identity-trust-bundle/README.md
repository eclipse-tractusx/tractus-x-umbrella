# Identity & Trust Bundle

The Identity & Trust Bundle provides identity management and authentication services for the Catena-X ecosystem. It includes the Identity Wallet Mock and OAuth2 Authorization Server.

## Components

- **Identity Wallet Mock**: Simulates identity wallet functionality for testing and development
- **OAuth2 Authorization Server**: Provides OAuth2 and OpenID Connect authentication services
- **Identity Provider Services**: Manages user identities and authentication

## Prerequisites

- Kubernetes cluster (version 1.24 or higher)
- Helm (version 3.8 or higher)
- kubectl configured to access your cluster

## Installation

### Standalone Installation

To install the Identity & Trust Bundle standalone:

```bash
# Add the repository
helm repo add tractusx https://eclipse-tractusx.github.io/charts/dev

# Install the bundle
helm install identity-trust-bundle ./charts/identity-trust-bundle
```

### Installation with Umbrella Chart

To install as part of the umbrella chart:

```bash
helm install umbrella ./charts/umbrella --set identity-trust-bundle.enabled=true
```

## Configuration

The bundle can be configured through the `values.yaml` file or using `--set` flags. Key configuration options include:

### Identity Wallet Mock Configuration

```yaml
identity-wallet-mock:
  enabled: true
  image:
    repository: eclipse-tractusx/identity-wallet-mock
    tag: "1.0.0"
  service:
    type: ClusterIP
    port: 8080
```

### OAuth2 Server Configuration

```yaml
oauth2-server:
  enabled: true
  config:
    oauth2:
      clients:
        - clientId: "your-client-id"
          clientSecret: "your-client-secret"
          redirectUris:
            - "http://your-app:8080/login/oauth2/code/oauth2"
```

## Usage

### Accessing the Identity Wallet Mock

After installation, the Identity Wallet Mock API will be available at:
```
http://<service-name>:8080
```

### OAuth2 Authentication Flow

1. Configure your application to use the OAuth2 server:
   ```
   Authorization URL: http://<oauth2-service>:8080/oauth2/authorize
   Token URL: http://<oauth2-service>:8080/oauth2/token
   ```

2. Use the provided client credentials to authenticate:
   ```bash
   curl -X POST http://<oauth2-service>:8080/oauth2/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret"
   ```

## Security

The bundle includes security features:
- OAuth2 and OpenID Connect authentication
- Secure token management
- DID-based identity verification
- Role-based access control

## Troubleshooting

Common issues and solutions:

1. **Authentication Issues**
   - Check OAuth2 server logs: `kubectl logs -l app.kubernetes.io/name=oauth2-server`
   - Verify client credentials and redirect URIs

2. **Identity Wallet Issues**
   - Check wallet service status: `kubectl get svc -l app.kubernetes.io/name=identity-wallet-mock`
   - Verify DID configuration and trusted issuers

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 