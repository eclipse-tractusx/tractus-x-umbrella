# HashiCorp Vault Secrets Setup Script

This script automates the creation of secrets in HashiCorp Vault from YAML configuration files using the **Vault HTTP
API with batch operations** for improved performance. It's designed to work with the Tractus-X Umbrella project's secret
structure.

## Features

- **YAML Parsing**: Reads secrets from YAML files with nested key-value structures
- **HTTP API Integration**: Uses Vault HTTP API for direct, efficient communication
- **Dry Run Mode**: Preview what would be created without making actual changes
- **Error Handling**: Comprehensive validation and error reporting
- **Flexible Configuration**: Configurable Vault paths and authentication methods

## Requirements

### Prerequisites

1. **Python 3.6+**: With required libraries
2. **Vault Access**: HTTP access to a Vault instance with valid token
3. **Network Connectivity**: Direct HTTP/HTTPS access to Vault server

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Vault Setup

Set the required environment variables:

```bash
# Set Vault server address
export VAULT_ADDR="http://your-vault-server:8200"

# Set Vault token
export VAULT_TOKEN="your-vault-token"
```

## Usage

### Basic Usage

```bash
# Create secrets from default file (dry run)
python vault-secrets-setup.py --dry-run

# Create secrets for real
python vault-secrets-setup.py

# Use custom YAML file
python vault-secrets-setup.py --yaml-file ../charts/umbrella/values-external-secrets.yaml

# Use custom Vault path
python vault-secrets-setup.py --vault-path custom/path
```

### Command Line Options

| Option          | Description                                       | Default              |
|-----------------|---------------------------------------------------|----------------------|
| `--yaml-file`   | Path to YAML file containing secrets              | `vault-secrets.yaml` |
| `--vault-path`  | Vault KV mount path                               | `secret`             |
| `--dry-run`     | Show what would be created without making changes | `false`              |
| `--verbose, -v` | Enable verbose output                             | `false`              |

### YAML File Format

The script expects a YAML file with the following structure:

```yaml
externalSecrets:
  secret-name-1:
    key1: value1
    key2: value2
  
  secret-name-2:
    username: admin
    password: secret123
  
  secret-name-3:
    api-key: abc123
    endpoint: https://api.example.com
```

### Example

Using the provided test file:

```bash
# Test with the sample secrets
python vault-secrets-setup.py --yaml-file vault-secrets.yaml --dry-run
```

This will process the following secrets:

- `umbrella-centralidp-postgresql`
- `umbrella-centralidp`
- `umbrella-centralidp-base-service-accounts`
- `umbrella-centralidp-clients`
- `umbrella-centralidp-extra-service-accounts`

## Output Examples

### Dry Run Output

```
HashiCorp Vault Secrets Setup (HTTP API)
========================================
✓ Skipping Vault configuration and connection checks (dry-run mode)
✓ Loaded 5 secret groups from vault-secrets.yaml

Found 5 secret groups to process:
  - umbrella-centralidp-postgresql
  - umbrella-centralidp
  - umbrella-centralidp-base-service-accounts
  - umbrella-centralidp-clients
  - umbrella-centralidp-extra-service-accounts

[DRY RUN MODE] - No actual changes will be made

Processing secrets...
----------------------------------------
[DRY RUN] Would create 5 secrets in parallel
[DRY RUN] Would create secret: secret/umbrella-centralidp-postgresql
[DRY RUN]   postgres-password=***
[DRY RUN]   password=***
----------------------------------------
Summary: 5/5 secrets processed successfully
```

### Production Output

```
HashiCorp Vault Secrets Setup (HTTP API)
========================================
✓ Vault HTTP API connection verified
✓ Token valid, policies: default, admin
✓ Loaded 5 secret groups from vault-secrets.yaml

Found 5 secret groups to process:
  - umbrella-centralidp-postgresql
  - umbrella-centralidp
  - umbrella-centralidp-base-service-accounts
  - umbrella-centralidp-clients
  - umbrella-centralidp-extra-service-accounts

Processing secrets...
----------------------------------------
Creating 5 secrets using 10 parallel workers...
✓ Created secret: secret/umbrella-centralidp-postgresql (2 keys)
✓ Created secret: secret/umbrella-centralidp (1 keys)
✓ Created secret: secret/umbrella-centralidp-base-service-accounts (19 keys)
✓ Created secret: secret/umbrella-centralidp-clients (4 keys)
✓ Created secret: secret/umbrella-centralidp-extra-service-accounts (16 keys)
Batch operation completed in 1.23 seconds
----------------------------------------
Summary: 5/5 secrets processed successfully
```

## HTTP API Operations

The script uses Vault HTTP API endpoints equivalent to:

```bash
# HTTP POST to Vault KV v2 API
POST /v1/secret/data/umbrella-centralidp-postgresql
{
  "data": {
    "postgres-password": "dbpasswordcentralidp",
    "password": "dbpasswordcentralidp"
  }
}

# Parallel processing for multiple secrets
# All requests sent concurrently for optimal performance
```

## Troubleshooting

### Common Issues

1. **"VAULT_ADDR environment variable not set"**
    - Set VAULT_ADDR to your Vault server URL
    - Example: `export VAULT_ADDR="http://localhost:8200"`

2. **"VAULT_TOKEN environment variable not set"**
    - Set VAULT_TOKEN to a valid Vault token
    - Example: `export VAULT_TOKEN="hvs.your-token-here"`

3. **"Cannot connect to Vault"**
    - Verify Vault server is running and accessible
    - Check network connectivity and firewall rules
    - Ensure VAULT_ADDR uses correct protocol (http/https)

4. **"Vault authentication failed (HTTP 403)"**
    - Verify VAULT_TOKEN is valid and not expired
    - Check token has write permissions to the target path
    - Review Vault policies and ACLs

5. **"No secrets found in YAML file"**
    - Verify YAML file structure matches expected format
    - Check for proper indentation and syntax

### Debug Mode

For additional debugging information, use the verbose flag:

```bash
python vault-secrets-setup.py --verbose --dry-run
```

## Contributing

When modifying the script:

1. Test with `--dry-run` first
2. Validate against different YAML structures
3. Update documentation for new features
4. Consider backward compatibility

## License

This script is part of the Tractus-X Umbrella project and follows the same licensing terms.