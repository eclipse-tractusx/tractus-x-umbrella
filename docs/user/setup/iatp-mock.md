# IATP Mock Setup (Optional)

This guide provides instructions to configure and enable the IATP Mock component, which serves as a placeholder for testing and simulating functionalities related to the IATP workflow.

## Precondition: Build the IATP Mock Docker Image

The IATP Mock requires a compatible Docker image. Follow these steps to build the image:

1. **Navigate to the IATP Mock Directory**:
   Clone the Umbrella Chart repository and navigate to the IATP Mock directory:
   ```bash
   git clone https://github.com/eclipse-tractusx/tractus-x-umbrella.git
   cd tractus-x-umbrella/iatp-mock/
   ```

2. **Build the Docker Image**:
   Run the following command to build the Docker image:
   ```bash
   docker build -t tractusx/iatp-mock:testing --platform linux/amd64 .
   ```

## Enabling IATP Mock

Once the Docker image is built, enable the IATP Mock in the Helm values file.

1. Update the `values.yaml` file to enable the `iatp-mock` component:
   ```yaml
   iatp-mock:
     enabled: true
   ```

2. Deploy the Umbrella Chart with the updated configuration:
   ```bash
   helm upgrade --install umbrella . --namespace umbrella --create-namespace
   ```

## Accessing IATP Mock

After deployment, the IATP Mock service will be accessible at the following endpoint:
```bash
http://iatpmock.tx.test
```

## Notes

- Verify that the `iatp-mock` component is running by checking the Kubernetes pods:
  ```bash
  kubectl get pods --namespace umbrella
  ```

- Use the IATP Mock service to simulate workflows and test integrations within the Catena-X ecosystem.

For further details, refer to the [Umbrella Chart repository](https://github.com/eclipse-tractusx/tractus-x-umbrella).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

* SPDX-License-Identifier: CC-BY-4.0
* SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation
* Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
