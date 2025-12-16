#!/bin/bash
# quickstart-azure.sh
# One-stop Azure deployment script
# Usage: ./quickstart-azure.sh [staging|production] [eastus|westus|etc]

set -euo pipefail

ENVIRONMENT=${1:-staging}
LOCATION=${2:-eastus}

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 The Hunter - Azure Deployment Quickstart${NC}"
echo ""
echo "Environment: $ENVIRONMENT"
echo "Location: $LOCATION"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check prerequisites
echo -e "${BLUE}[1/4] Checking prerequisites...${NC}"
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Install: https://aka.ms/azure-cli"
    exit 1
fi
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install: https://docker.com"
    exit 1
fi
if ! command -v jq &> /dev/null; then
    echo "❌ jq not found. Install: https://stedolan.github.io/jq/"
    exit 1
fi
echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# Deploy infrastructure
echo -e "${BLUE}[2/4] Deploying Azure infrastructure...${NC}"
cd "$SCRIPT_DIR"
bash deploy-to-azure.sh "$ENVIRONMENT" "$LOCATION" || {
    echo "❌ Deployment failed"
    exit 1
}
echo -e "${GREEN}✓ Infrastructure deployed${NC}"
echo ""

# Build and push images
echo -e "${BLUE}[3/4] Building and pushing Docker images...${NC}"
bash build-and-push.sh || {
    echo "❌ Build failed"
    exit 1
}
echo -e "${GREEN}✓ Images pushed to Azure Container Registry${NC}"
echo ""

# Generate secrets instruction
echo -e "${BLUE}[4/4] GitHub secrets configuration${NC}"
echo ""
echo "Run these commands in your repository:"
echo ""
bash "${SCRIPT_DIR}/github-secrets.sh" 2>/dev/null || true
echo ""
echo -e "${GREEN}✓ All steps complete!${NC}"
echo ""
echo "🎉 Your calculator is being deployed to Azure!"
echo ""
echo "Status:"
grep -E "(apiUrl|frontendUrl)" "${SCRIPT_DIR}/deployment-outputs.json" 2>/dev/null || echo "See deployment-outputs.json for URLs"
