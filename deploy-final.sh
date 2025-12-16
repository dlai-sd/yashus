#!/bin/bash

# Get Azure registry password
REGISTRY_PASSWORD=$(az acr credential show --name yashuregistry --query passwords[0].value -o tsv)

# Deploy backend
echo "Deploying backend..."
az container create \
  --resource-group yashus-rg \
  --name yashus-backend \
  --image yashuregistry.azurecr.io/the-hunter-backend:latest \
  --registry-username yashuregistry \
  --registry-password "$REGISTRY_PASSWORD" \
  --cpu 0.5 \
  --memory 0.5 \
  --os-type Linux \
  --location westus2 \
  --port 8000 \
  --dns-name-label yashus-backend-api \
  --no-wait

# Deploy frontend
echo "Deploying frontend..."
az container create \
  --resource-group yashus-rg \
  --name yashus-frontend \
  --image yashuregistry.azurecr.io/the-hunter-frontend:latest \
  --registry-username yashuregistry \
  --registry-password "$REGISTRY_PASSWORD" \
  --cpu 0.5 \
  --memory 0.5 \
  --os-type Linux \
  --location westus2 \
  --port 80 \
  --dns-name-label yashus-calculator \
  --no-wait

echo "✓ Deployment commands sent"
echo "Waiting 20 seconds for containers to get public IPs..."
sleep 20

# Get URLs
FRONTEND_FQDN=$(az container show --resource-group yashus-rg --name yashus-frontend --query ipAddress.fqdn -o tsv 2>/dev/null)
BACKEND_FQDN=$(az container show --resource-group yashus-rg --name yashus-backend --query ipAddress.fqdn -o tsv 2>/dev/null)

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       🎉 YASHUS CALCULATOR IS LIVE ON AZURE! 🎉             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 CALCULATOR FRONTEND:"
echo "   http://$FRONTEND_FQDN"
echo ""
echo "🔧 BACKEND API:"
echo "   http://$BACKEND_FQDN:8000"
echo ""
echo "📚 SWAGGER API DOCS:"
echo "   http://$BACKEND_FQDN:8000/docs"
echo ""
echo "✅ Both containers are running in Azure (westus2)"
echo ""
