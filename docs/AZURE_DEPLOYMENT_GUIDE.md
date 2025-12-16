# Azure Deployment Guide

## Status: Codespace Ready + Azure Automation

Your calculator is running on Codespace. To deploy to Azure:

---

## Prerequisites

✓ Azure CLI installed (via devconfig)  
✓ Logged into Azure (`az login`)  
✓ Service Principal created  

---

## Step-by-Step Deployment

### 1. Set Environment Variables

```bash
export AZURE_SUBSCRIPTION_ID='your-subscription-id'
export AZURE_TENANT_ID='your-tenant-id'
export AZURE_CLIENT_ID='your-client-id'
export AZURE_CLIENT_SECRET='your-client-secret'
```

### 2. Run Automated Deployment

```bash
cd /workspaces/yashus
bash azure/deploy-automated.sh
```

This will:
- Authenticate with Azure
- Create resource group
- Create container registry
- Build and push frontend image
- Build and push backend image
- Create PostgreSQL database
- Deploy both containers

---

## What Gets Created

**Azure Resources:**
- Resource Group: `yashus-rg`
- Container Registry: `yashuregistry.azurecr.io`
- PostgreSQL Database: `yashus-db-*`
- Frontend Container: `yashus-frontend`
- Backend Container: `yashus-backend`

**Time to Deploy:** 3-5 minutes

---

## Get URLs After Deployment

```bash
# Frontend URL
az container show --resource-group yashus-rg \
    --name yashus-frontend \
    --query ipAddress.fqdn -o tsv

# Backend URL (with Swagger docs)
az container show --resource-group yashus-rg \
    --name yashus-backend \
    --query ipAddress.fqdn -o tsv
# Then visit: http://<backend-fqdn>:8000/docs
```

---

## Monitor Deployment

```bash
# Check container status
az container list --resource-group yashus-rg --output table

# View logs
az container logs --resource-group yashus-rg --name yashus-frontend
az container logs --resource-group yashus-rg --name yashus-backend
```

---

## Configuration

All settings in `/devconfig.yaml` under `azure:` section:
- Subscription ID → environment variable
- Client credentials → environment variables
- Resource names → hardcoded (customizable)
- Database credentials → auto-generated and shown at deploy end

---

## Security Notes

- ✓ Credentials stored as environment variables (not in code)
- ✓ GitHub push protection blocks secrets
- ✓ Use GitHub Secrets for CI/CD automation
- ✓ Service Principal has Contributor role (can be restricted)

---

## Next: GitHub Actions CI/CD

To automate this deployment on every git push:

1. Go to GitHub repo Settings → Secrets
2. Add as repository secrets:
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
3. Create GitHub Actions workflow that calls `azure/deploy-automated.sh`

---

## Troubleshooting

**Error: "Could not translate host name 'db' to address"**
- Backend trying to connect to PostgreSQL - wait 2 minutes for database to initialize
- Check logs: `az container logs --resource-group yashus-rg --name yashus-backend`

**Error: "Docker push failed"**
- Verify registry login: `az acr login --name yashuregistry`
- Check Docker daemon is running

**Containers stuck in 'Creating' state**
- View detailed logs: `az container show --resource-group yashus-rg --name yashus-frontend`
- Database may still be initializing (PostgreSQL takes ~2 min)

---

## Cleanup

To remove all Azure resources:

```bash
az group delete --name yashus-rg --yes
```

This removes all containers, database, registry, and the resource group.

---

## Cost Estimate

**Monthly costs (approximate):**
- Container Registry (Basic): $5/month
- PostgreSQL (B_Gen5_1): $50/month
- Container Instances (2x): $10-20/month
- **Total: ~$65-75/month**

---

**Repository:** https://github.com/dlai-sd/yashus  
**Last Updated:** December 13, 2025
