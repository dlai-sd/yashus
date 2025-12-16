# 🚀 THE HUNTER - DEPLOYMENT SUMMARY

## ✅ Current Status: READY FOR DEPLOYMENT

Your application is fully built and pushed to Azure Container Registry. The images are ready to run.

---

## 📦 Docker Images Ready in ACR

**Registry:** `thehunterregistry.azurecr.io`

### Backend API
- **Image:** `the-hunter-api:latest`
- **Size:** ~261MB (optimized multi-stage build)
- **Status:** ✅ Pushed and verified
- **Port:** 8000
- **Tech:** Python 3.11, FastAPI, SQLAlchemy

### Frontend
- **Image:** `the-hunter-frontend:latest`
- **Size:** ~150MB (optimized incremental build)
- **Status:** ✅ Pushed and verified
- **Port:** 80
- **Tech:** Angular 17, Node 18

---

## 🚧 Azure Deployment Blocked

**Reason:** Azure quota limit reached in eastus region
```
Limit: 4 StandardCores in eastus
Usage: 4 StandardCores (100%)
Needed: 1 StandardCore
```

### Solutions:

#### Option 1: Wait for Quota (FREE)
Azure quotas reset daily. Try again after 24 hours.

#### Option 2: Request Quota Increase
1. Go to [Azure Portal](https://portal.azure.com)
2. Search "Quotas"
3. Filter: Container Instances, eastus
4. Request increase for "StandardCores"
5. Usually approved in 1-2 hours

#### Option 3: Use Different Region
The containers can be deployed in westus, westus2, or northeurope.

#### Option 4: Use App Service Instead
Deploy on Azure App Service (higher tier limit):

```bash
# Delete current ACR
az acr delete -n thehunterregistry -g the-hunter-staging --yes

# Create new simpler deployment
az appservice plan create \
  -g the-hunter-staging \
  -n the-hunter-plan \
  --sku B1 \
  --is-linux

# Deploy frontend
az webapp create \
  -g the-hunter-staging \
  -n the-hunter-frontend \
  --plan the-hunter-plan \
  --deployment-container-image-name "$REGISTRY/the-hunter-frontend:latest"
```

---

## 🏃 Local Alternative: Run Locally First

Test the full application locally before deploying to Azure:

```bash
# Start all services (database + API + frontend)
cd /workspaces/yashus/TheHunter
docker-compose up

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

---

## 📋 When Quota is Available

### Auto-Deploy Script

```bash
python3 /workspaces/yashus/deploy_aci_optimized.py
```

### Manual Deploy

```bash
RESOURCE_GROUP="the-hunter-staging"
REGISTRY="thehunterregistry.azurecr.io"
REGION="eastus"

# Get ACR credentials
ACR_PASS=$(az acr credential show -n thehunterregistry -g $RESOURCE_GROUP --query 'passwords[0].value' -o tsv)

# Deploy backend
az container create \
  --resource-group $RESOURCE_GROUP \
  --name the-hunter-api \
  --image $REGISTRY/the-hunter-api:latest \
  --cpu 0.5 \
  --memory 0.5 \
  --ports 8000 \
  --registry-login-server $REGISTRY \
  --registry-username thehunterregistry \
  --registry-password "$ACR_PASS" \
  --os-type Linux \
  --no-wait

# Deploy frontend
az container create \
  --resource-group $RESOURCE_GROUP \
  --name the-hunter-frontend \
  --image $REGISTRY/the-hunter-frontend:latest \
  --cpu 0.5 \
  --memory 0.5 \
  --ports 80 \
  --registry-login-server $REGISTRY \
  --registry-username thehunterregistry \
  --registry-password "$ACR_PASS" \
  --os-type Linux \
  --no-wait

# Check status
az container show -g $RESOURCE_GROUP -n the-hunter-api --query '{state:instanceView.state, ip:ipAddress.ip}'
az container show -g $RESOURCE_GROUP -n the-hunter-frontend --query '{state:instanceView.state, ip:ipAddress.ip}'
```

---

## 🎯 Expected Output When Deployed

```
🎉 DEPLOYMENT SUCCESSFUL - BOTH CONTAINERS RUNNING!

📊 ACCESS YOUR APPLICATION:

CALCULATOR FRONTEND:
  URL: http://{public-ip}
  Direct: http://{public-ip}/calculator

BACKEND API:
  URL: http://{api-ip}:8000
  Docs: http://{api-ip}:8000/docs
  Health: http://{api-ip}:8000/api/v1/calculator/health
```

---

## 🔐 Credentials & Configuration

### Azure Setup
```
Subscription: 72c36f52-fba9-40f9-96ea-6724f8ed0d8a
Tenant: c4e57f2c-9337-49ba-8deb-286d0a29677b
Resource Group: the-hunter-staging
Registry: thehunterregistry.azurecr.io
```

### Application Config
```
DATABASE_URL: sqlite:///./hunter.db (default)
SECRET_KEY: the-hunter-secret-key-2024
DEBUG: False
```

---

## 📝 Next Steps

1. **Check quota** in 24 hours and retry deployment
2. **OR** request quota increase (1-2 hours)
3. **OR** run locally to test fully
4. **OR** use different region/service tier

---

## 🆘 Troubleshooting

### Container fails to start
```bash
# Check logs
az container logs -g the-hunter-staging -n the-hunter-api

# Restart
az container restart -g the-hunter-staging -n the-hunter-api
```

### Can't connect to API from frontend
1. Ensure `API_BASE_URL` env var is set correctly
2. Check backend is healthy: `curl http://{api-ip}:8000/api/v1/calculator/health`
3. Verify CORS settings in backend

### Images not pulling
```bash
# Verify login
az acr login --name thehunterregistry

# Check image exists
az acr repository list --name thehunterregistry
```

---

## 📊 Deployment Files

- **Deploy Script:** `/workspaces/yashus/deploy_aci_optimized.py`
- **Docker Compose:** `/workspaces/yashus/TheHunter/docker-compose.yml`
- **Backend Image:** `thehunterregistry.azurecr.io/the-hunter-api:latest`
- **Frontend Image:** `thehunterregistry.azurecr.io/the-hunter-frontend:latest`

---

**Status:** ✅ Ready to deploy once quota is available
**Last Updated:** December 13, 2025
**Deployment Time Est:** 5-10 minutes once quota is freed
