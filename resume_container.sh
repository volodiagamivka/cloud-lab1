# Configuration Variables
RESOURCE_GROUP="hospital-rg"
LOCATION="eastus"
ACR_NAME="hospitalacrregistry"
CONTAINER_APP_ENV="hospital-env"
CONTAINER_APP_NAME="hospital-app"
IMAGE_NAME="hospital-flask-app"
IMAGE_TAG="latest"

MYSQL_HOST="labsserver.mysql.database.azure.com"
MYSQL_ADMIN_USER="volgam"
MYSQL_ADMIN_PASSWORD="Gamivka1505"
MYSQL_DATABASE="hospital"
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# 0. Check Azure Account
az account show > /dev/null

# 1. Check and Create Resource Group
if ! az group show --name "$RESOURCE_GROUP" &>/dev/null; then
    az group create --name "$RESOURCE_GROUP" --location "$LOCATION" > /dev/null
fi

# 2. Check and Create ACR
ACR_RG=""
ACR_RG=$(az acr list --query "[?name=='$ACR_NAME'].resourceGroup" -o tsv | head -n 1)

if [ -z "$ACR_RG" ]; then
    if az acr create \
      --resource-group "$RESOURCE_GROUP" \
      --name "$ACR_NAME" \
      --sku Basic \
      --admin-enabled true 2>/dev/null; then
        ACR_RG="$RESOURCE_GROUP"
    else
        ALTERNATIVE_ACR_NAME=$(az acr list --query "[0].name" -o tsv)
        ALTERNATIVE_ACR_RG=$(az acr list --query "[0].resourceGroup" -o tsv)
        if [ -n "$ALTERNATIVE_ACR_NAME" ] && [ -n "$ALTERNATIVE_ACR_RG" ]; then
            ACR_NAME="$ALTERNATIVE_ACR_NAME"
            ACR_RG="$ALTERNATIVE_ACR_RG"
        else
            ACR_NAME="${ACR_NAME}$(date +%s | tail -c 5)"
            az acr create \
              --resource-group "$RESOURCE_GROUP" \
              --name "$ACR_NAME" \
              --sku Basic \
              --admin-enabled true > /dev/null
            ACR_RG="$RESOURCE_GROUP"
        fi
    fi
fi

# Get ACR Credentials
ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$ACR_RG" --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --resource-group "$ACR_RG" --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --resource-group "$ACR_RG" --query passwords[0].value --output tsv)

# 3. Check, Build, and Push Docker Image
IMAGE_EXISTS=false
if az acr repository show-tags --name "$ACR_NAME" --repository "$IMAGE_NAME" &>/dev/null; then
    if az acr repository show-tags --name "$ACR_NAME" --repository "$IMAGE_NAME" --query "[?name=='$IMAGE_TAG']" -o tsv | grep -q "$IMAGE_TAG"; then
        IMAGE_EXISTS=true
    fi
fi

if [ "$IMAGE_EXISTS" = false ]; then
    docker build --platform linux/amd64 -t "$IMAGE_NAME:$IMAGE_TAG" . > /dev/null
    az acr login --name "$ACR_NAME" > /dev/null
    docker tag "$IMAGE_NAME:$IMAGE_TAG" "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
    docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG" > /dev/null
fi

# 4. Check and Create Container Apps Environment
ENV_RG=""
ENV_RG=$(az containerapp env list --query "[?name=='$CONTAINER_APP_ENV' && resourceGroup=='$RESOURCE_GROUP'].resourceGroup" -o tsv | head -n 1)

if [ -z "$ENV_RG" ]; then
    EXISTING_ENV=$(az containerapp env list --query "[0].{Name:name, RG:resourceGroup}" -o tsv)
    if [ -n "$EXISTING_ENV" ]; then
        EXISTING_ENV_NAME=$(echo "$EXISTING_ENV" | cut -f1)
        EXISTING_ENV_RG=$(echo "$EXISTING_ENV" | cut -f2)
        
        if [ "$EXISTING_ENV_RG" != "$RESOURCE_GROUP" ]; then
            SUBSCRIPTION_ID=$(az account show --query id -o tsv)
            ENV_FULL_ID="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$EXISTING_ENV_RG/providers/Microsoft.App/managedEnvironments/$EXISTING_ENV_NAME"
            APPS_IN_ENV=$(az containerapp list --query "[?properties.environmentId=='$ENV_FULL_ID'].{Name:name, RG:resourceGroup}" -o tsv)
            
            if [ -n "$APPS_IN_ENV" ]; then
                echo "$APPS_IN_ENV" | while read APP_NAME APP_RG; do
                    if [ -n "$APP_NAME" ] && [ -n "$APP_RG" ]; then
                        az containerapp delete --name "$APP_NAME" --resource-group "$APP_RG" --yes 2>/dev/null || true
                    fi
                done
                sleep 20
            fi
            
            az containerapp env delete --name "$EXISTING_ENV_NAME" --resource-group "$EXISTING_ENV_RG" --yes 2>/dev/null || true
            sleep 30
        fi
    fi
    
    if az containerapp env create \
      --name "$CONTAINER_APP_ENV" \
      --resource-group "$RESOURCE_GROUP" \
      --location "$LOCATION" > /dev/null; then
        ENV_RG="$RESOURCE_GROUP"
    else
        exit 1
    fi
else
    ENV_RG="$RESOURCE_GROUP"
fi

# 5. Check and Create Container App
if ! az containerapp show --name "$CONTAINER_APP_NAME" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
    ENV_ID=$(az containerapp env show --name "$CONTAINER_APP_ENV" --resource-group "$RESOURCE_GROUP" --query id -o tsv)
    if az containerapp create \
      --name "$CONTAINER_APP_NAME" \
      --resource-group "$RESOURCE_GROUP" \
      --environment "$ENV_ID" \
      --image "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG" \
      --registry-server "$ACR_LOGIN_SERVER" \
      --registry-username "$ACR_USERNAME" \
      --registry-password "$ACR_PASSWORD" \
      --target-port 5000 \
      --ingress external \
      --min-replicas 1 \
      --max-replicas 10 \
      --cpu 0.5 \
      --memory 1.0Gi \
      --secrets \
        "db-host=${MYSQL_HOST}" \
        "db-user=${MYSQL_ADMIN_USER}" \
        "db-password=${MYSQL_ADMIN_PASSWORD}" \
        "db-name=${MYSQL_DATABASE}" \
        "db-port=3306" \
        "secret-key=${SECRET_KEY}" \
      --env-vars \
        "DB_HOST=secretref:db-host" \
        "DB_USER=secretref:db-user" \
        "DB_PASSWORD=secretref:db-password" \
        "DB_NAME=secretref:db-name" \
        "DB_PORT=secretref:db-port" \
        "SECRET_KEY=secretref:secret-key" > /dev/null; then
        sleep 30
    else
        exit 1
    fi
fi

# 6. Wait for Container App Readiness
MAX_WAIT=300
WAIT_TIME=0
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    STATUS=$(az containerapp show --name "$CONTAINER_APP_NAME" --resource-group "$RESOURCE_GROUP" --query properties.runningStatus -o tsv 2>/dev/null)
    PROVISIONING=$(az containerapp show --name "$CONTAINER_APP_NAME" --resource-group "$RESOURCE_GROUP" --query properties.provisioningState -o tsv 2>/dev/null)
    
    if [ "$STATUS" = "Running" ] && [ "$PROVISIONING" = "Succeeded" ]; then
        break
    fi
    
    sleep 10
    WAIT_TIME=$((WAIT_TIME + 10))
done

# 7. Configure Autoscaling
RETRY_COUNT=0
MAX_RETRIES=5
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if az containerapp update \
      --name "$CONTAINER_APP_NAME" \
      --resource-group "$RESOURCE_GROUP" \
      --scale-rule-name http-scale \
      --scale-rule-type http \
      --scale-rule-http-concurrency 50 2>/dev/null; then
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            sleep 20
        fi
    fi
done

APP_URL=$(az containerapp show \
  --name "$CONTAINER_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query properties.configuration.ingress.fqdn \
  --output tsv 2>/dev/null)

# Final Output: URL
if [ -n "$APP_URL" ] && [ "$APP_URL" != "null" ]; then
    echo "   Swagger: https://$APP_URL/swagger/"
    
fi