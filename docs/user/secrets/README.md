# Secrets Management in Tractus-X Umbrella

This documentation covers the secrets management capabilities in the Tractus-X Umbrella chart, including the External
Secrets Operator integration and HashiCorp Vault connectivity.

## Overview

The Tractus-X Umbrella chart provides comprehensive secrets management through:

- **External Secrets Operator (ESO)**: Kubernetes operator that integrates external secret management systems
- **HashiCorp Vault Integration**: Secure secret storage and retrieval from Vault
- **Secret Replacement**: Automatic replacement of hardcoded secrets with external references
- **Flexible Authentication**: Support for multiple Vault authentication methods

## Key Components

### External Secrets Operator

The External Secrets Operator is a Kubernetes operator that integrates external secret management systems like HashiCorp
Vault, AWS Secrets Manager, Azure Key Vault, and others. In the Tractus-X Umbrella, it's used to:

- Fetch secrets from HashiCorp Vault
- Create Kubernetes secrets automatically
- Keep secrets synchronized with external sources
- Provide fallback mechanisms for development environments

### Secret Replacement Mechanism

The umbrella chart implements a sophisticated secret replacement system that:

- Replaces hardcoded secrets in values files with external secret references
- Supports both Vault-backed and fake secrets for testing
- Maintains backward compatibility with existing deployments
- Provides seamless integration across all Tractus-X components

### HashiCorp Vault Integration

Vault serves as the primary external secret store, offering:

- Centralized secret management
- Fine-grained access control
- Audit logging
- Secret versioning and rotation
- Multiple authentication methods (Token, AppRole)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │ External Secrets │    │  HashiCorp      │
│   Secrets       │◄───│    Operator      │◄───│    Vault        │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                        ▲                       ▲
         │                        │                       │
         │              ┌─────────────────┐               │
         └──────────────│  SecretStore    │───────────────┘
                        │  Configuration  │
                        └─────────────────┘
```

## Documentation Structure

This documentation is organized into the following sections:

- **[Deployment Guide](deployment.md)**: Step-by-step deployment instructions
- **[Vault Setup](vault-setup.md)**: HashiCorp Vault configuration and connection
- **[Configuration Reference](configuration.md)**: Complete configuration options and examples
- **[Connected Services](connected-services.md)**: Documentation for services using secrets
- **[Troubleshooting](troubleshooting.md)**: Common issues and solutions

## Quick Start

1. **Enable External Secrets**: Set `external-secrets.enabled: true` in your values file
2. **Configure Vault**: Set up Vault connection parameters
3. **Deploy Secrets**: Use the vault-secrets-setup script to populate Vault
4. **Deploy Umbrella**: Install the umbrella chart with external secrets enabled

For detailed instructions, see the [Deployment Guide](deployment.md).

## Security Considerations

- Always use HTTPS for Vault communication in production
- Implement proper Vault policies and access controls
- Regularly rotate Vault tokens and secrets
- Enable Vault audit logging
- Use namespace isolation for multi-tenant deployments

## Support

For issues and questions:

- Check the [Troubleshooting Guide](troubleshooting.md)
- Review the Tractus-X documentation
- Open an issue in the Tractus-X Umbrella repository