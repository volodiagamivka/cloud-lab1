#!/bin/bash

# --- Configuration Variables ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

RESOURCE_GROUP="labs"
LOCATION="polandcentral"
ACR_NAME="boychukdbregistry"
CONTAINER_APP_NAME="boychuk-repos-app"
CONTAINER_APP_ENV="boychuk-repos-env"
IMAGE_NAME="flask-rest-api"
IMAGE_TAG="latest"

DB_HOST="${DB_HOST:-hospserver.mysql.database.azure.com}"
DB_USER="${DB_USER:-boychuk}"
DB_PASSWORD="${DB_PASSWORD:-Maks_mia3}"
DB_NAME="${DB_NAME:-hospitalss}"

# --- Helper Functions ---
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# --- Pre-check ---
if ! command -v az &> /dev/null; then
    error "Azure CLI not found. Install it: https://docs.microsoft.com/cli/azure/install-azure-cli"
fi

log "Starting Azure deployment..."

# --- Azure Authentication ---
log "Checking Azure authentication..."
az account show &> /dev/null || az login

# --- Resource Providers ---
log "Registering resource providers..."
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait
az provider register --namespace Microsoft.ContainerRegistry --wait
log "Resource providers registered"

# --- Resource Group ---
log "Creating Resource Group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION --output none

# --- Azure Container Registry (ACR) ---
log "Checking for existing ACR: $ACR_NAME"
ACR_EXISTS=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP 2>/dev/null)

if [ -z "$ACR_EXISTS" ]; then
    log "Creating new Azure Container Registry: $ACR_NAME"
    az acr create \
        --resource-group $RESOURCE_GROUP \
        --name $ACR_NAME \
        --sku Basic \
        --admin-enabled true \
        --output none
    
    if [ $? -ne 0 ]; then
        error "Failed to create ACR. Check if the name '$ACR_NAME' is globally unique."
    fi
    log "ACR created successfully"
else
    log "ACR already exists, enabling admin and proceeding."
    az acr update --name $ACR_NAME --admin-enabled true --output none
fi

# --- Docker Build and Push ---
log "Logging into Azure Container Registry..."
az acr login --name $ACR_NAME || error "Failed to log into ACR"

log "Building Docker image for linux/amd64..."
docker buildx build --platform linux/amd64 -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -ne 0 ]; then
    warning "Buildx failed, attempting standard build with --platform..."
    docker build --platform linux/amd64 -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} .
    
    if [ $? -ne 0 ]; then
        error "Failed to build Docker image"
    fi
fi
log "Docker image built successfully for linux/amd64"

log "Publishing image to Azure Container Registry..."
docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} || error "Failed to push image to ACR"
log "Image successfully uploaded to ACR"

# --- Get ACR Credentials ---
log "Fetching ACR credentials..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv 2>/dev/null)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv 2>/dev/null)

if [ -z "$ACR_USERNAME" ] || [ -z "$ACR_PASSWORD" ]; then
    error "Failed to retrieve ACR credentials. Ensure admin-enabled=true."
fi
log "Credentials retrieved for user: $ACR_USERNAME"

# --- Container Apps Environment ---
log "Checking for existing Container Apps Environment..."
ENV_EXISTS=$(az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP 2>/dev/null)

if [ -z "$ENV_EXISTS" ]; then
    log "Creating new Container Apps Environment: $CONTAINER_APP_ENV"
    az containerapp env create \
        --name $CONTAINER_APP_ENV \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION \
        --output none || error "Failed to create Container Apps Environment"
    log "Environment created successfully"
else
    log "Environment already exists, proceeding."
fi

# --- Container App Deployment ---
log "Checking for existing Container App: $CONTAINER_APP_NAME"
APP_EXISTS=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP 2>/dev/null)

if [ -n "$APP_EXISTS" ]; then
    warning "Container App exists, deleting old one..."
    az containerapp delete \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --yes \
        --output none
    log "Old Container App deleted"
fi

log "Creating new Container App with autoscaling..."
az containerapp create \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_APP_ENV \
    --image ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} \
    --registry-server ${ACR_NAME}.azurecr.io \
    --registry-username "$ACR_USERNAME" \
    --registry-password "$ACR_PASSWORD" \
    --target-port 5000 \
    --ingress external \
    --min-replicas 1 \
    --max-replicas 10 \
    --cpu 0.5 \
    --memory 1.0Gi \
    --env-vars \
        DB_HOST="$DB_HOST" \
        DB_USER="$DB_USER" \
        DB_PASSWORD="$DB_PASSWORD" \
        DB_NAME="$DB_NAME" \
        PORT=5000 \
    --output none || error "Failed to create Container App"
log "Container App created successfully"

# --- Autoscaling Rules Configuration ---
log "Configuring autoscaling rules..."

SCALE_CONFIG_FILE=$(mktemp)
cat > "$SCALE_CONFIG_FILE" <<EOF
{
  "minReplicas": 1,
  "maxReplicas": 10,
  "rules": [
    {
      "name": "http-scaling",
      "http": {
        "metadata": {
          "concurrentRequests": "10"
        }
      }
    },
    {
      "name": "cpu-scaling",
      "custom": {
        "type": "cpu",
        "metadata": {
          "type": "Utilization",
          "value": "70"
        }
      }
    }
  ]
}
EOF

log "Applying scaling configuration..."
az containerapp update \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --set "properties.template.scale=@$SCALE_CONFIG_FILE" \
    --output none || error "Failed to configure autoscaling"

rm -f "$SCALE_CONFIG_FILE"

log "Autoscaling rules configured"

# --- Output and Cleanup ---
log "Retrieving application URL..."
APP_URL=$(az containerapp show \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query properties.configuration.ingress.fqdn -o tsv)

if [ -z "$APP_URL" ]; then
    warning "Failed to retrieve application URL"
    APP_URL="unknown"
fi

log "=========================================="
log "Deployment completed successfully!"
log "=========================================="
log "Application URL: https://$APP_URL"
log "Swagger URL: https://$APP_URL/api/docs/"
log "Resource Group: $RESOURCE_GROUP"
log "Container App: $CONTAINER_APP_NAME"
log "Autoscaling: min=1, max=10, HTTP >10 concurrent requests, CPU >70%"
log "=========================================="

echo "APP_URL=https://$APP_URL" > .env.azure
log "URL saved to .env.azure"