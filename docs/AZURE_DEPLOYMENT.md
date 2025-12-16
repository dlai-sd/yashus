# Azure Deployment Guide

## Pre-Deployment Requirements

### 1. Azure Resources Setup

```bash
# Set variables
RESOURCE_GROUP="the-hunter-rg"
LOCATION="eastus"
REGISTRY_NAME="thehunterregistry"
APP_SERVICE_PLAN="the-hunter-plan"
APP_SERVICE_API="the-hunter-api-prod"
APP_SERVICE_FRONTEND="the-hunter-frontend-prod"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Container Registry
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $REGISTRY_NAME \
  --sku Basic \
  --admin-enabled true

# Create App Service Plan
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Create Web App for API
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $APP_SERVICE_API \
  --deployment-container-image-name-user placeholder

# Create Web App for Frontend
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $APP_SERVICE_FRONTEND \
  --deployment-container-image-name-user placeholder

# Create PostgreSQL Database
az postgres server create \
  --resource-group $RESOURCE_GROUP \
  --name the-hunter-db \
  --location $LOCATION \
  --admin-user hunter \
  --admin-password <STRONG_PASSWORD> \
  --sku-name B_Gen5_1 \
  --storage-size 51200
```

### 2. GitHub Secrets Setup

Go to GitHub Repository → Settings → Secrets and variables → Actions

Add these secrets:

```
AZURE_CREDENTIALS: <Service Principal JSON>
AZURE_REGISTRY_USERNAME: <Registry Username>
AZURE_REGISTRY_PASSWORD: <Registry Password>
AZURE_RESOURCE_GROUP: the-hunter-rg
STAGING_DATABASE_URL: postgresql://hunter:password@host/hunter_db
DEPLOYED_URL: https://the-hunter-api-prod.azurewebsites.net
```

### 3. Create Service Principal

```bash
az ad sp create-for-rbac \
  --name the-hunter-deployment \
  --role Contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/the-hunter-rg \
  --json-auth
```

## Manual Deployment Steps

### 1. Build and Push Docker Images

```bash
# Login to Azure Container Registry
az acr login --name thehunterregistry

# Build API image
docker build -t thehunterregistry.azurecr.io/the-hunter-api:latest \
  ./TheHunter/backend

# Build Frontend image
docker build -t thehunterregistry.azurecr.io/the-hunter-frontend:latest \
  ./TheHunter/frontend

# Push images
docker push thehunterregistry.azurecr.io/the-hunter-api:latest
docker push thehunterregistry.azurecr.io/the-hunter-frontend:latest
```

### 2. Deploy API

```bash
# Set environment variables on App Service
az webapp config appsettings set \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod \
  --settings \
    DATABASE_URL="postgresql://..." \
    DEBUG="false" \
    SECRET_KEY="..." \
    ALLOWED_ORIGINS="https://the-hunter-frontend-prod.azurewebsites.net"

# Configure Docker image source
az webapp config container set \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod \
  --docker-custom-image-name thehunterregistry.azurecr.io/the-hunter-api:latest \
  --docker-registry-server-url https://thehunterregistry.azurecr.io \
  --docker-registry-server-user <USERNAME> \
  --docker-registry-server-password <PASSWORD>

# Restart app
az webapp restart \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod
```

### 3. Deploy Frontend

```bash
# Configure Docker image source
az webapp config container set \
  --resource-group the-hunter-rg \
  --name the-hunter-frontend-prod \
  --docker-custom-image-name thehunterregistry.azurecr.io/the-hunter-frontend:latest \
  --docker-registry-server-url https://thehunterregistry.azurecr.io \
  --docker-registry-server-user <USERNAME> \
  --docker-registry-server-password <PASSWORD>

# Restart app
az webapp restart \
  --resource-group the-hunter-rg \
  --name the-hunter-frontend-prod
```

## Automated Deployment via GitHub Actions

The workflow is in `.github/workflows/deploy.yml` and is manually triggered.

**To deploy:**

1. Go to GitHub Actions tab
2. Select "Build & Deploy - Manual Trigger"
3. Click "Run workflow"
4. Choose environment: `staging` or `production`
5. Monitor progress in the workflow run

## Health Checks & Monitoring

```bash
# Check API health
curl https://the-hunter-api-prod.azurewebsites.net/api/v1/calculator/health

# View logs
az webapp log tail \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod

# Stream logs in real-time
az webapp log tail \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod \
  --follow
```

## Database Migration on Azure

```bash
# Run database migrations in container
az webapp ssh \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod

# Inside container:
# python -m alembic upgrade head
```

## Rollback Strategy

```bash
# Rollback to previous image tag
az webapp config container set \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod \
  --docker-custom-image-name thehunterregistry.azurecr.io/the-hunter-api:previous-tag

# Restart
az webapp restart \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod
```

## Cost Optimization

- **App Service Plan**: Use B1 (Basic) for development, scale to B2/B3 for production
- **Database**: Start with B_Gen5_1, upgrade as needed
- **Storage**: Enable automatic backups and set retention
- **Container Registry**: Basic tier is sufficient, enable Auto-delete for old images

## Troubleshooting

**Application won't start:**
```bash
# Check logs
az webapp log show \
  --resource-group the-hunter-rg \
  --name the-hunter-api-prod
```

**Database connection failed:**
```bash
# Verify database firewall rules
az postgres server firewall-rule list \
  --resource-group the-hunter-rg \
  --server-name the-hunter-db
```

**Performance issues:**
```bash
# Check metrics
az monitor metrics list \
  --resource /subscriptions/<ID>/resourceGroups/the-hunter-rg/providers/Microsoft.Web/sites/the-hunter-api-prod \
  --metric "CpuPercentage,MemoryPercentage"
```
