#!/bin/bash
set -e

# Deploy to Azure using environment variables for credentials
# Set these from GitHub Secrets in CI/CD or from your shell

SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-}"
TENANT_ID="${AZURE_TENANT_ID:-}"
CLIENT_ID="${AZURE_CLIENT_ID:-}"
CLIENT_SECRET="${AZURE_CLIENT_SECRET:-}"

if [ -z "$SUBSCRIPTION_ID" ] || [ -z "$CLIENT_ID" ]; then
    echo "ERROR: Missing Azure credentials"
    echo ""
    echo "Required environment variables:"
    echo "  AZURE_SUBSCRIPTION_ID"
    echo "  AZURE_TENANT_ID"
    echo "  AZURE_CLIENT_ID"
    echo "  AZURE_CLIENT_SECRET"
    echo ""
    echo "Example:"
    echo "  export AZURE_SUBSCRIPTION_ID='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
    echo "  export AZURE_TENANT_ID='yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy'"
    echo "  export AZURE_CLIENT_ID='zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz'"
    echo "  export AZURE_CLIENT_SECRET='your-client-secret'"
    echo "  bash azure/deploy-automated.sh"
    exit 1
fi

RESOURCE_GROUP="yashus-rg"
LOCATION="eastus"
REGISTRY_NAME="yashuregistry"
REGISTRY_URL="${REGISTRY_NAME}.azurecr.io"
REPO_ROOT="/workspaces/yashus"

echo "=========================================="
echo "The Hunter - Azure Deployment"
echo "=========================================="
echo ""
echo "Subscription: ${SUBSCRIPTION_ID:0:8}..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Region: $LOCATION"
echo ""

# Step 1: Authenticate
echo "Step 1: Authenticating with Azure..."
az login --service-principal \
    -u "$CLIENT_ID" \
    -p "$CLIENT_SECRET" \
    --tenant "$TENANT_ID" > /dev/null 2>&1
az account set --subscription "$SUBSCRIPTION_ID"
echo "  [OK] Authenticated"

# Step 2: Create resource group
echo ""
echo "Step 2: Creating resource group..."
if ! az group exists --name "$RESOURCE_GROUP" | grep -q true; then
    az group create \
        --name "$RESOURCE_GROUP" \
        --location "$LOCATION" > /dev/null 2>&1
fi
echo "  [OK] Resource group: $RESOURCE_GROUP"

# Step 3: Create registry
echo ""
echo "Step 3: Creating container registry..."
if ! az acr show --resource-group "$RESOURCE_GROUP" --name "$REGISTRY_NAME" &>/dev/null; then
    az acr create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$REGISTRY_NAME" \
        --sku Basic > /dev/null 2>&1
fi
echo "  [OK] Registry: $REGISTRY_URL"

# Step 4: Build and push frontend
echo ""
echo "Step 4: Building and pushing frontend..."
cd "$REPO_ROOT/TheHunter/frontend"
docker build -t $REGISTRY_URL/the-hunter-frontend:latest . > /dev/null 2>&1
az acr login --name "$REGISTRY_NAME" > /dev/null 2>&1
docker push $REGISTRY_URL/the-hunter-frontend:latest > /dev/null 2>&1
echo "  [OK] Frontend image pushed"

# Step 5: Build and push backend
echo ""
echo "Step 5: Building and pushing backend..."
cd "$REPO_ROOT/TheHunter/backend"
docker build -t $REGISTRY_URL/the-hunter-backend:latest . > /dev/null 2>&1
docker push $REGISTRY_URL/the-hunter-backend:latest > /dev/null 2>&1
echo "  [OK] Backend image pushed"

# Step 6: Create PostgreSQL database
echo ""
echo "Step 6: Creating PostgreSQL database..."
DB_NAME="yashus-db-$(date +%s)"
DB_PASSWORD=$(openssl rand -base64 32 | tr -d '/' | cut -c1-25)
az postgres server create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$DB_NAME" \
    --location "$LOCATION" \
    --admin-user dbadmin \
    --admin-password "$DB_PASSWORD" \
    --sku-name B_Gen5_1 \
    --storage-size 102400 > /dev/null 2>&1
echo "  [OK] Database: $DB_NAME"

# Step 7: Deploy frontend container
echo ""
echo "Step 7: Deploying frontend container..."
az container create \
    --resource-group "$RESOURCE_GROUP" \
    --name yashus-frontend \
    --image $REGISTRY_URL/the-hunter-frontend:latest \
    --registry-login-server $REGISTRY_URL \
    --registry-username "$CLIENT_ID" \
    --registry-password "$CLIENT_SECRET" \
    --cpu 1 \
    --memory 1.5 \
    --ports 80 \
    --environment-variables API_BASE_URL="http://yashus-backend:8000" \
    --no-wait > /dev/null 2>&1
echo "  [OK] Frontend deployment started"

# Step 8: Deploy backend container
echo ""
echo "Step 8: Deploying backend container..."
DATABASE_URL="postgresql://dbadmin:$DB_PASSWORD@${DB_NAME}.postgres.database.azure.com/yashus"
az container create \
    --resource-group "$RESOURCE_GROUP" \
    --name yashus-backend \
    --image $REGISTRY_URL/the-hunter-backend:latest \
    --registry-login-server $REGISTRY_URL \
    --registry-username "$CLIENT_ID" \
    --registry-password "$CLIENT_SECRET" \
    --cpu 1 \
    --memory 1.5 \
    --ports 8000 \
    --environment-variables DATABASE_URL="$DATABASE_URL" \
    --no-wait > /dev/null 2>&1
echo "  [OK] Backend deployment started"

echo ""
echo "=========================================="
echo "DEPLOYMENT INITIATED"
echo "=========================================="
echo ""
echo "Containers are starting (takes 1-2 minutes)..."
echo ""
echo "Check status:"
echo "  az container list --resource-group $RESOURCE_GROUP --output table"
echo ""
echo "View logs:"
echo "  az container logs --resource-group $RESOURCE_GROUP --name yashus-frontend"
echo "  az container logs --resource-group $RESOURCE_GROUP --name yashus-backend"
echo ""
echo "Get URLs (after containers start):"
echo "  az container show --resource-group $RESOURCE_GROUP --name yashus-frontend --query ipAddress.fqdn"
echo "  az container show --resource-group $RESOURCE_GROUP --name yashus-backend --query ipAddress.fqdn"
echo ""
echo "Database credentials:"
echo "  Server: ${DB_NAME}.postgres.database.azure.com"
echo "  User: dbadmin"
echo "  Password: $DB_PASSWORD (SAVE THIS)"
