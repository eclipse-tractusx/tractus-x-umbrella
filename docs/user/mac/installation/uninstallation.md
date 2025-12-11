# Uninstallation

This guide provides instructions to remove the Umbrella Chart and its associated resources from your Kubernetes cluster.

## Basic Uninstallation

To uninstall the Umbrella Chart, run the following command:

```bash
helm delete umbrella --namespace umbrella
```

This command removes all the resources created by the Helm release in the specified namespace.

## Additional Cleanup

If persistence was enabled during installation, the persistent volume claims (PVCs) and associated persistent volumes (PVs) are not automatically deleted. To manually clean up these resources:

1. List the PVCs in the namespace:

   ```bash
   kubectl get pvc --namespace umbrella
   ```

2. Delete the PVCs:

   ```bash
   kubectl delete pvc <pvc-name> --namespace umbrella
   ```

3. Optionally, delete any remaining PVs:

   ```bash
   kubectl get pv
   kubectl delete pv <pv-name>
   ```

## Namespace Cleanup

If you want to remove the entire namespace, including all remaining resources:

```bash
kubectl delete namespace umbrella
```

## Notes

- Ensure that no other applications are using the namespace before deleting it.
- Use the cleanup steps carefully to avoid accidental data loss.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
