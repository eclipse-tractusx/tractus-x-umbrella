#!/bin/bash

set -o errexit
set -o errtrace
set -o pipefail
set -o nounset


## This script install/upgrade the EDCs based on the following parameterized values.


## PARAMETERS
CLUSTER_CONTEXT=$1                  ## the current k8s cluster where the edc is to be deployed    
DEPLOYMENT_NAME=$2                  ## helm deployment name e.g, umbrella-edc
DEPLOYMENT_TYPE=$3                  ## install/upgrade
HELM_VALUES_FILE=$4                 ## the relative path to the helm values.yaml
NAMESPACE=$5                        ## the namespace where the edc is to be deployed
# DOMAIN_NAME=$6                    ## the domain name for the public facing ingress

SUB_DIR="charts/umbrella"
DEFAULT_VALUES_FILE="values.yaml"

########## Kubernetes environment configurations Start ###################

if command -v kubectl &> /dev/null
then
    echo "kubectl is already installed on this machine"
    kubectl version --client
else
    echo "kubectl is not installed, installing Kubectl..."
    curl -LO -s "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

    # Make it executable
    chmod +x kubectl

    # Move to a directory in your PATH
    sudo mv kubectl /usr/local/bin/

    # Verify installation
    kubectl version --client

    echo "kubectl installed successfully!"

    ## kubectl version check
    echo "Checking kubectl version..."
    echo `kubectl version`
fi


## change the kube context
kubectl config use-context $CLUSTER_CONTEXT

########## Kubernetes environment configurations End ###################


########## Helm deployment configurations Start ###################

cd ../$SUB_DIR
echo "Working directory is now `pwd`"
echo ""

#echo "Updating helm repositories..."
#helm repo update
#echo ""

echo "Getting dependencies from Repo ..."
echo ""
#helm repo add tractusx-dev https://eclipse-tractusx.github.io/charts/dev
#echo ""

helm dependency update ../tx-data-provider
helm dependency update
echo "Now installing customised configuration stored in $HELM_VALUES_FILE ..."
echo "Be patient, will take a while ..."

if [[ $DEPLOYMENT_TYPE == "install" ]]
then
    echo "Installing the deployment..."
    helm $DEPLOYMENT_TYPE $DEPLOYMENT_NAME -f $HELM_VALUES_FILE --namespace $NAMESPACE --debug .

elif [[ $DEPLOYMENT_TYPE == "upgrade" ]]
then
    echo "Upgrading the deployment..."
    helm $DEPLOYMENT_TYPE -i $DEPLOYMENT_NAME -f $HELM_VALUES_FILE --namespace $NAMESPACE --debug .
else
    echo "Invalid deployment type -> accepted types -> (install or upgrade)"
fi


########## Helm deployment configurations End ###################

echo "Script execution Finished!!"
