#!/bin/bash

BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Port forwarding${NC}"
kubectl port-forward svc/lab-vault 8200:8200 -n lab &
kubectl port-forward svc/lab-dapsserver 4567:4567 -n lab &
kubectl port-forward svc/lab-edcprovider-controlplane 6080:8080 6181:8181 -n lab &
kubectl port-forward svc/lab-edcconsumer-controlplane 7080:8080 7181:8181 -n lab &
kubectl port-forward svc/semantic-hub 8088:8080 -n lab &
kubectl port-forward svc/cx-lab-registry-svc 10200:8080 -n lab &
kubectl port-forward svc/keycloak 4011:8080 -n lab &
kubectl port-forward svc/irs-provider-backend 10199:8080 -n lab &
kubectl port-forward svc/lab-minio-console 9001:9001 -n lab &
kubectl port-forward svc/lab-irs 8080:8080 -n lab &
kubectl port-forward svc/irs-frontend 3000:8080 -n lab