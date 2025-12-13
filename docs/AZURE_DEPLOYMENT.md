# Azure Deployment Guide

## Prerequisites

1. **Azure Account**: Active Azure subscription
2. **Azure CLI**: Installed and configured
3. **Docker Hub Account**: For storing container images
4. **GitHub Repository**: With admin access for setting secrets

## Step 1: Set Up Azure Resources

### 1.1 Login to Azure

```bash
az login
```

### 1.2 Create Resource Group

```bash
az group create \
  --name yashus-rg \
  --location eastus
```

### 1.3 Create PostgreSQL Database

```bash
az postgres flexible-server create \
  --resource-group yashus-rg \
  --name yashus-db \
  --location eastus \
  --admin-user yashusadmin \
  --admin-password <your-secure-password> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 15 \
  --storage-size 32 \
  --public-access 0.0.0.0

# Create database
az postgres flexible-server db create \
  --resource-group yashus-rg \
  --server-name yashus-db \
  --database-name yashus
```

### 1.4 Create Redis Cache

```bash
az redis create \
  --resource-group yashus-rg \
  --name yashus-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0 \
  --enable-non-ssl-port
```

## Step 2: Configure GitHub Secrets

Go to your repository settings → Secrets → Actions and add:

### Required Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AZURE_CREDENTIALS` | Azure service principal credentials | JSON object |
| `AZURE_RESOURCE_GROUP` | Azure resource group name | `yashus-rg` |
| `DOCKER_USERNAME` | Docker Hub username | `your-username` |
| `DOCKER_PASSWORD` | Docker Hub password/token | `your-token` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://...` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | `sk-...` |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key (optional) | `AIza...` |

### 2.1 Create Azure Service Principal

```bash
az ad sp create-for-rbac \
  --name yashus-sp \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/yashus-rg \
  --sdk-auth
```

Copy the JSON output and save it as `AZURE_CREDENTIALS` secret.

### 2.2 Get Database Connection String

```bash
az postgres flexible-server show-connection-string \
  --server-name yashus-db \
  --database-name yashus \
  --admin-user yashusadmin \
  --query connectionStrings.psql_asyncpg
```

### 2.3 Get Redis Connection String

```bash
az redis show \
  --resource-group yashus-rg \
  --name yashus-redis \
  --query hostName -o tsv

az redis list-keys \
  --resource-group yashus-rg \
  --name yashus-redis \
  --query primaryKey -o tsv
```

Format: `redis://:password@hostname:6379/0`

## Step 3: Deploy Application

### Option 1: Via GitHub Actions (Recommended)

1. Push code to `main` branch:
```bash
git push origin main
```

2. GitHub Actions will automatically:
   - Run tests
   - Build Docker images
   - Push to Docker Hub
   - Deploy to Azure Container Instances

### Option 2: Manual Deployment

#### 3.1 Build and Push Docker Images

```bash
# Backend
cd backend
docker build -t your-username/yashus-backend:latest .
docker push your-username/yashus-backend:latest

# Frontend
cd ../frontend
docker build -t your-username/yashus-frontend:latest .
docker push your-username/yashus-frontend:latest
```

#### 3.2 Deploy to Azure Container Instances

```bash
# Deploy Backend
az container create \
  --resource-group yashus-rg \
  --name yashus-backend \
  --image your-username/yashus-backend:latest \
  --dns-name-label yashus-backend \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL='postgresql+asyncpg://...' \
    REDIS_URL='redis://...' \
    SECRET_KEY='your-secret-key' \
    OPENAI_API_KEY='sk-...' \
    GOOGLE_MAPS_API_KEY='AIza...'

# Deploy Frontend
az container create \
  --resource-group yashus-rg \
  --name yashus-frontend \
  --image your-username/yashus-frontend:latest \
  --dns-name-label yashus-frontend \
  --ports 80 4200
```

## Step 4: Configure Custom Domain (Optional)

### 4.1 Get Container IPs

```bash
az container show \
  --resource-group yashus-rg \
  --name yashus-backend \
  --query ipAddress.fqdn -o tsv

az container show \
  --resource-group yashus-rg \
  --name yashus-frontend \
  --query ipAddress.fqdn -o tsv
```

### 4.2 Configure DNS

Add CNAME records in your DNS provider:
- `api.yashus.in` → Backend FQDN
- `app.yashus.in` → Frontend FQDN

### 4.3 Set Up SSL (via Azure Application Gateway)

```bash
az network application-gateway create \
  --resource-group yashus-rg \
  --name yashus-gateway \
  --location eastus \
  --capacity 2 \
  --sku Standard_v2 \
  --public-ip-address yashus-public-ip \
  --vnet-name yashus-vnet \
  --subnet gateway-subnet
```

## Step 5: Set Up Monitoring

### 5.1 Enable Application Insights

```bash
az monitor app-insights component create \
  --resource-group yashus-rg \
  --app yashus-insights \
  --location eastus \
  --application-type web
```

### 5.2 Configure Log Analytics

```bash
az monitor log-analytics workspace create \
  --resource-group yashus-rg \
  --workspace-name yashus-logs \
  --location eastus
```

## Step 6: Verify Deployment

### 6.1 Check Container Status

```bash
az container show \
  --resource-group yashus-rg \
  --name yashus-backend \
  --query instanceView.state

az container show \
  --resource-group yashus-rg \
  --name yashus-frontend \
  --query instanceView.state
```

### 6.2 View Logs

```bash
# Backend logs
az container logs \
  --resource-group yashus-rg \
  --name yashus-backend

# Frontend logs
az container logs \
  --resource-group yashus-rg \
  --name yashus-frontend
```

### 6.3 Test Endpoints

```bash
# Get backend URL
BACKEND_URL=$(az container show \
  --resource-group yashus-rg \
  --name yashus-backend \
  --query ipAddress.fqdn -o tsv)

# Test health endpoint
curl "http://${BACKEND_URL}:8000/health"

# Test API
curl "http://${BACKEND_URL}:8000/api/v1/agents/"
```

## Step 7: Scaling and Optimization

### 7.1 Scale Container Instances

```bash
# Update backend to use more resources
az container create \
  --resource-group yashus-rg \
  --name yashus-backend \
  --image your-username/yashus-backend:latest \
  --cpu 2 \
  --memory 4 \
  --dns-name-label yashus-backend \
  --ports 8000
```

### 7.2 Use Azure Container Apps (Alternative)

For better scaling and management:

```bash
az containerapp env create \
  --resource-group yashus-rg \
  --name yashus-env \
  --location eastus

az containerapp create \
  --resource-group yashus-rg \
  --name yashus-backend-app \
  --environment yashus-env \
  --image your-username/yashus-backend:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 5
```

## Troubleshooting

### Issue: Container fails to start

**Solution:** Check logs and environment variables
```bash
az container logs --resource-group yashus-rg --name yashus-backend
az container show --resource-group yashus-rg --name yashus-backend
```

### Issue: Database connection fails

**Solution:** Check firewall rules
```bash
az postgres flexible-server firewall-rule create \
  --resource-group yashus-rg \
  --name yashus-db \
  --rule-name AllowAllAzureIPs \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Issue: Redis connection timeout

**Solution:** Enable non-SSL port or configure SSL
```bash
az redis update \
  --resource-group yashus-rg \
  --name yashus-redis \
  --set enableNonSslPort=true
```

## Cost Optimization

### 1. Use Azure Reserved Instances
- Save up to 72% with 1-3 year commitments

### 2. Auto-shutdown Development Resources
```bash
az container stop \
  --resource-group yashus-rg \
  --name yashus-backend
```

### 3. Use Azure Spot Instances
- For non-critical workloads, save up to 90%

### 4. Monitor Costs
```bash
az consumption usage list \
  --start-date 2024-01-01 \
  --end-date 2024-01-31
```

## Maintenance

### Update Application

```bash
# Update backend
az container delete --resource-group yashus-rg --name yashus-backend --yes
az container create ... # Use create command with latest image

# Or use GitHub Actions by pushing to main branch
```

### Backup Database

```bash
az postgres flexible-server backup list \
  --resource-group yashus-rg \
  --server-name yashus-db

# Manual backup
pg_dump -h yashus-db.postgres.database.azure.com \
  -U yashusadmin \
  -d yashus > backup.sql
```

### Monitor Performance

```bash
# CPU and memory usage
az monitor metrics list \
  --resource /subscriptions/<sub-id>/resourceGroups/yashus-rg/providers/Microsoft.ContainerInstance/containerGroups/yashus-backend \
  --metric CPUUsage \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z
```

## Security Best Practices

1. **Use Key Vault for Secrets**
```bash
az keyvault create \
  --resource-group yashus-rg \
  --name yashus-vault \
  --location eastus

az keyvault secret set \
  --vault-name yashus-vault \
  --name database-password \
  --value "your-secure-password"
```

2. **Enable HTTPS Only**
3. **Use Managed Identities**
4. **Regular Security Updates**
5. **Enable Azure Defender**

## Support

For issues with Azure deployment:
- Azure Support: https://azure.microsoft.com/support/
- Documentation: https://docs.microsoft.com/azure/
- Community: https://stackoverflow.com/questions/tagged/azure

---

**Last Updated**: December 2024
