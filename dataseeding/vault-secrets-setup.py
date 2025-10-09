#  Copyright (c) 2025 Contributors to the Eclipse Foundation
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  This program and the accompanying materials are made available under the
#  terms of the Apache License, Version 2.0 which is available at
#  https://www.apache.org/licenses/LICENSE-2.0.
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#
#  SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python3
"""
HashiCorp Vault Secrets Setup Script

This script reads secrets from a YAML file and creates them in HashiCorp Vault
using the Vault HTTP API with batch operations for improved performance.
The YAML structure should have top-level keys as secret names
and nested key-value pairs as the secret properties.

Requirements:
- VAULT_ADDR environment variable set
- VAULT_TOKEN environment variable set
- PyYAML library installed (pip install PyYAML)
- requests library installed (pip install requests)

Usage:
    python vault-secrets-setup.py [--yaml-file path/to/secrets.yaml] [--vault-path secret] [--dry-run]
"""

import argparse
import os
import sys
import time
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
import requests


def get_vault_config():
    """Get Vault configuration from environment variables."""
    vault_addr = os.getenv('VAULT_ADDR')
    vault_token = os.getenv('VAULT_TOKEN')
    
    if not vault_addr:
        print("✗ Error: VAULT_ADDR environment variable not set")
        return None, None
    
    if not vault_token:
        print("✗ Error: VAULT_TOKEN environment variable not set")
        return None, None
    
    return vault_addr, vault_token


def check_vault_connection(vault_addr: str, vault_token: str):
    """Check if Vault is accessible via HTTP API."""
    try:
        headers = {"X-Vault-Token": vault_token}
        response = requests.get(f"{vault_addr}/v1/auth/token/lookup-self", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            token_info = response.json()
            print(f"✓ Vault HTTP API connection verified")
            print(f"✓ Token valid, policies: {', '.join(token_info.get('data', {}).get('policies', []))}")
            return True
        else:
            print(f"✗ Error: Vault authentication failed (HTTP {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: Cannot connect to Vault at {vault_addr}: {e}")
        return False


def load_yaml_secrets(yaml_file: str) -> Dict[str, Any]:
    """Load secrets from YAML file."""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not isinstance(data, dict):
            raise ValueError("YAML file must contain a dictionary at root level")
        
        print(f"✓ Loaded {len(data)} secret groups from {yaml_file}")
        return data
    except FileNotFoundError:
        print(f"✗ Error: YAML file not found: {yaml_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"✗ Error: Invalid YAML format: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading YAML file: {e}")
        sys.exit(1)


def create_vault_secret_http(vault_addr: str, vault_token: str, secret_name: str, 
                            secret_data: Dict[str, Any], vault_path: str, dry_run: bool = False) -> bool:
    """Create a secret in Vault using HTTP API."""
    full_path = f"{vault_path}/{secret_name}"
    
    if dry_run:
        print(f"[DRY RUN] Would create secret: {full_path}")
        for key, value in secret_data.items():
            print(f"[DRY RUN]   {key}=***")
        return True
    
    try:
        headers = {
            "X-Vault-Token": vault_token,
            "Content-Type": "application/json"
        }
        
        # For KV v2 engine, the API path includes /data/
        api_url = f"{vault_addr}/v1/{vault_path}/data/{secret_name}"
        payload = {"data": secret_data}
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code in [200, 204]:
            print(f"✓ Created secret: {full_path} ({len(secret_data)} keys)")
            return True
        else:
            error_msg = response.text if response.text else f"HTTP {response.status_code}"
            print(f"✗ Error creating secret {full_path}: {error_msg}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error creating secret {full_path}: {e}")
        return False


def create_secrets_batch(vault_addr: str, vault_token: str, secrets: Dict[str, Any], 
                        vault_path: str, dry_run: bool = False, max_workers: int = 10) -> tuple:
    """Create multiple secrets in parallel using HTTP API."""
    if dry_run:
        print(f"[DRY RUN] Would create {len(secrets)} secrets in parallel")
        for secret_name, secret_data in secrets.items():
            create_vault_secret_http(vault_addr, vault_token, secret_name, secret_data, vault_path, dry_run)
        return len(secrets), 0
    
    print(f"Creating {len(secrets)} secrets using {max_workers} parallel workers...")
    start_time = time.time()
    
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_secret = {
            executor.submit(create_vault_secret_http, vault_addr, vault_token, 
                          secret_name, secret_data, vault_path, dry_run): secret_name
            for secret_name, secret_data in secrets.items()
        }
        
        # Process completed tasks
        for future in as_completed(future_to_secret):
            secret_name = future_to_secret[future]
            try:
                success = future.result()
                if success:
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                print(f"✗ Exception processing {secret_name}: {e}")
                failed_count += 1
    
    duration = time.time() - start_time
    print(f"Batch operation completed in {duration:.2f} seconds")
    
    return success_count, failed_count


def extract_secrets_from_yaml(yaml_file: str) -> Dict[str, Any]:
    """Extract secrets from the specific YAML structure used in the project."""
    data = load_yaml_secrets(yaml_file)
    
    # The secrets are nested under various keys, we need to find the actual secret definitions
    # Based on the file structure, secrets seem to be at the root level after some metadata
    secrets = {}
    
    external_secrets = data.get("externalSecrets")
    if external_secrets is None:
        print("YAML does not contain 'externalSecrets' key. No secrets to process.")
        return secrets
    if not isinstance(external_secrets, dict):
        print("'externalSecrets' key is present but is not a mapping/dict. No secrets to process.")
        return secrets

    for key, value in external_secrets.items():
        if isinstance(value, dict):
            # Check if this is one of our target secrets or looks like a secret
            if all(isinstance(v, (str, int, float, bool)) for v in value.values()):
                secrets[key] = value
    
    return secrets


def main():
    parser = argparse.ArgumentParser(
        description='Create HashiCorp Vault secrets from YAML file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--yaml-file', 
        default='vault-secrets.yaml',
        help='Path to YAML file containing secrets (default: vault-secrets.yaml)'
    )
    
    parser.add_argument(
        '--vault-path',
        default='secret',
        help='Vault KV mount path (default: secret)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without actually creating secrets'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print("HashiCorp Vault Secrets Setup (HTTP API)")
    print("=" * 40)
    
    # Get Vault configuration (skip in dry-run mode)
    if not args.dry_run:
        vault_addr, vault_token = get_vault_config()
        if not vault_addr or not vault_token:
            sys.exit(1)
        
        # Check prerequisites
        if not check_vault_connection(vault_addr, vault_token):
            sys.exit(1)
    else:
        print("✓ Skipping Vault configuration and connection checks (dry-run mode)")
        vault_addr, vault_token = "http://localhost:8200", "dummy-token"
    
    # Load and extract secrets
    try:
        secrets = extract_secrets_from_yaml(args.yaml_file)
        
        if not secrets:
            print("✗ No secrets found in YAML file")
            sys.exit(1)
        
        print(f"\nFound {len(secrets)} secret groups to process:")
        for secret_name in secrets.keys():
            print(f"  - {secret_name}")
        
        if args.dry_run:
            print("\n[DRY RUN MODE] - No actual changes will be made")
        
        print("\nProcessing secrets...")
        print("-" * 40)
        
        # Use batch processing for better performance
        success_count, failed_count = create_secrets_batch(
            vault_addr, vault_token, secrets, args.vault_path, args.dry_run
        )
        
        total_count = len(secrets)
        
        print("-" * 40)
        print(f"Summary: {success_count}/{total_count} secrets processed successfully")
        if failed_count > 0:
            print(f"Failed: {failed_count} secrets")
        
        if success_count < total_count:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n✗ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
