#!/bin/bash

# Exit on error
set -e

# Variables
RESOURCE_GROUP="your_resource_group"
ACR_NAME="your_acr_name"
APP_SERVICE_PLAN="your_app_service_plan"
WEB_APP_NAME="your_web_app_name"
DOCKER_IMAGE="your_docker_image"

# Login to Azure
echo "Logging in to Azure..."
az login

# Read variables from existing Azure resource group
echo "Reading variables from existing Azure resource group..."
RESOURCE_GROUP=$(az group show --name $RESOURCE_GROUP --query name --output tsv)
ACR_NAME=$(az acr show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query name --output tsv)
APP_SERVICE_PLAN=$(az appservice plan show --resource-group $RESOURCE_GROUP --name $APP_SERVICE_PLAN --query name --output tsv)
WEB_APP_NAME=$(az webapp show --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --query name --output tsv)

# Create Resource Group
echo "Creating Resource Group..."
az group create --name $RESOURCE_GROUP --location eastus

# Create Azure Container Registry (ACR)
echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Login to ACR
echo "Logging in to ACR..."
az acr login --name $ACR_NAME

# Build Docker image
echo "Building Docker image..."
docker build -t $ACR_NAME.azurecr.io/$DOCKER_IMAGE:latest .

# Push Docker image to ACR
echo "Pushing Docker image to ACR..."
docker push $ACR_NAME.azurecr.io/$DOCKER_IMAGE:latest

# Create App Service Plan
echo "Creating App Service Plan..."
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create Web App
echo "Creating Web App..."
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $WEB_APP_NAME --deployment-container-image-name $ACR_NAME.azurecr.io/$DOCKER_IMAGE:latest

# Configure Web App to use ACR
echo "Configuring Web App to use ACR..."
az webapp config container set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name $ACR_NAME.azurecr.io/$DOCKER_IMAGE:latest --docker-registry-server-url https://$ACR_NAME.azurecr.io

# Restart Web App
echo "Restarting Web App..."
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

echo "Deployment completed successfully!"
