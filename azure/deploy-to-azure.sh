#!/bin/bash
# deploy-to-azure.sh
# Automated Azure deployment using Bicep templates
# One command to deploy everything: resource group, registry, database, containers

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENVIRONMENT=${1:-staging}
LOCATION=${2:-eastus}

SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID:-}
RESOURCE_GROUP="the-hunter-${ENVIRONMENT}"
DB_PASSWORD=${AZURE_DB_PASSWORD:-}
SECRET_KEY=${AZURE_SECRET_KEY:-}

# Validate inputs
validate_inputs() {
    log_info "Validating inputs..."
    
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI not installed. Install from: https://aka.ms/azure-cli"
        exit 1
    fi
    
    if [ -z "$SUBSCRIPTION_ID" ]; then
        log_error "AZURE_SUBSCRIPTION_ID not set"
        echo "Set it: export AZURE_SUBSCRIPTION_ID=<your-subscription-id>"
        exit 1
    fi
    
    if [ -z "$DB_PASSWORD" ]; then
        log_warn "AZURE_DB_PASSWORD not set, using default (NOT recommended for production)"
        DB_PASSWORD="YourSecurePassword123!"
    fi
    
    if [ -z "$SECRET_KEY" ]; then
        log_warn "AZURE_SECRET_KEY not set, using default (NOT recommended for production)"
        SECRET_KEY="your-super-secret-key-change-this"
    fi
    
    log_success "Inputs validated"
}

# Set Azure subscription
set_subscription() {
    log_info "Setting Azure subscription..."
    
    az account set --subscription "$SUBSCRIPTION_ID" || {
        log_error "Failed to set subscription"
        exit 1
    }
    
    log_success "Subscription set"
}

# Create resource group
create_resource_group() {
    log_info "Creating resource group: $RESOURCE_GROUP..."
    
    az group create \
        --name "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --tags environment="$ENVIRONMENT" project="the-hunter" \
        || log_warn "Resource group may already exist"
    
    log_success "Resource group ready"
}

# Build and push Docker images
build_and_push_images() {
    log_info "Building Docker images..."
    
    cd "$PROJECT_ROOT"
    
    # Get registry name (will be created by bicep, but we need it for push)
    REGISTRY_NAME="thehunterregistry"
    REGISTRY_URL="${REGISTRY_NAME}.azurecr.io"
    
    log_info "Logging into Azure Container Registry..."
    az acr login --name "$REGISTRY_NAME" || {
        log_warn "ACR doesn't exist yet, skipping pre-push. Images will be pulled after creation."
        return 0
    }
    
    log_info "Building backend image..."
    docker build -t "$REGISTRY_URL/the-hunter-api:latest" \
        -f TheHunter/backend/Dockerfile \
        TheHunter/backend
    
    log_info "Pushing backend image..."
    docker push "$REGISTRY_URL/the-hunter-api:latest"
    
    log_info "Building frontend image..."
    docker build -t "$REGISTRY_URL/the-hunter-frontend:latest" \
        -f TheHunter/frontend/Dockerfile \
        TheHunter/frontend
    
    log_info "Pushing frontend image..."
    docker push "$REGISTRY_URL/the-hunter-frontend:latest"
    
    log_success "Images built and pushed"
}

# Deploy via Bicep
deploy_bicep() {
    log_info "Deploying Azure infrastructure via Bicep..."
    
    cd "${SCRIPT_DIR}"
    
    DEPLOYMENT_NAME="the-hunter-${ENVIRONMENT}-$(date +%s)"
    
    DEPLOYMENT_OUTPUT=$(az deployment group create \
        --name "$DEPLOYMENT_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --template-file main.bicep \
        --parameters parameters.json \
        --parameters environment="$ENVIRONMENT" \
        --parameters dbAdminPassword="$DB_PASSWORD" \
        --parameters secretKey="$SECRET_KEY" \
        --query 'properties.outputs' \
        -o json) || {
        log_error "Bicep deployment failed"
        exit 1
    }
    
    log_success "Bicep deployment complete"
    
    # Save outputs
    echo "$DEPLOYMENT_OUTPUT" > "${SCRIPT_DIR}/deployment-outputs.json"
    log_success "Outputs saved to deployment-outputs.json"
    
    echo "$DEPLOYMENT_OUTPUT"
}

# Extract and display outputs
extract_outputs() {
    log_info "Extracting deployment outputs..."
    
    local outputs_file="${SCRIPT_DIR}/deployment-outputs.json"
    
    if [ ! -f "$outputs_file" ]; then
        log_error "Deployment outputs not found"
        return 1
    fi
    
    echo ""
    echo "=========================================="
    echo "DEPLOYMENT OUTPUTS"
    echo "=========================================="
    
    REGISTRY_LOGIN_SERVER=$(jq -r '.registryLoginServer.value' "$outputs_file")
    REGISTRY_USERNAME=$(jq -r '.registryUsername.value' "$outputs_file")
    REGISTRY_PASSWORD=$(jq -r '.registryPassword.value' "$outputs_file")
    DATABASE_CONNECTION=$(jq -r '.databaseConnectionString.value' "$outputs_file")
    API_URL=$(jq -r '.apiUrl.value' "$outputs_file")
    FRONTEND_URL=$(jq -r '.frontendUrl.value' "$outputs_file")
    
    echo "Registry Login Server: $REGISTRY_LOGIN_SERVER"
    echo "Registry Username: $REGISTRY_USERNAME"
    echo "Registry Password: [REDACTED]"
    echo "Database Connection: [REDACTED - stored in secrets]"
    echo "API URL: $API_URL"
    echo "Frontend URL: $FRONTEND_URL"
    echo "=========================================="
    echo ""
    
    # Return for next steps
    echo "$REGISTRY_LOGIN_SERVER|$REGISTRY_USERNAME|$REGISTRY_PASSWORD|$DATABASE_CONNECTION|$API_URL|$FRONTEND_URL"
}

# Generate GitHub secrets
generate_github_secrets() {
    log_info "Generating GitHub secrets configuration..."
    
    local outputs_file="${SCRIPT_DIR}/deployment-outputs.json"
    local secrets_file="${SCRIPT_DIR}/github-secrets.sh"
    
    cat > "$secrets_file" << 'EOF'
#!/bin/bash
# Auto-generated GitHub secrets setup script
# Run this: bash github-secrets.sh

echo "Setting up GitHub secrets..."

REGISTRY_USERNAME=$(jq -r '.registryUsername.value' deployment-outputs.json)
REGISTRY_PASSWORD=$(jq -r '.registryPassword.value' deployment-outputs.json)
DATABASE_URL=$(jq -r '.databaseConnectionString.value' deployment-outputs.json)
RESOURCE_GROUP="the-hunter-staging"

# Note: AZURE_CREDENTIALS requires service principal setup
# See docs/AZURE_DEPLOYMENT.md for manual setup

echo "Run these commands in your repository:"
echo ""
echo "gh secret set AZURE_REGISTRY_USERNAME --body '$REGISTRY_USERNAME'"
echo "gh secret set AZURE_REGISTRY_PASSWORD --body '$REGISTRY_PASSWORD'"
echo "gh secret set AZURE_RESOURCE_GROUP --body '$RESOURCE_GROUP'"
echo "gh secret set STAGING_DATABASE_URL --body '$DATABASE_URL'"
echo ""
echo "For AZURE_CREDENTIALS, follow: docs/AZURE_DEPLOYMENT.md"
EOF
    
    chmod +x "$secrets_file"
    log_success "GitHub secrets script created: github-secrets.sh"
}

# Main workflow
main() {
    echo ""
    log_info "Starting The Hunter Azure Deployment"
    echo ""
    
    validate_inputs
    set_subscription
    create_resource_group
    
    # Note: Image build/push happens after resources exist
    # For now, we deploy and then build images
    
    deploy_bicep
    extract_outputs
    generate_github_secrets
    
    echo ""
    log_success "Azure infrastructure deployed successfully! 🎉"
    echo ""
    echo "Next steps:"
    echo "1. Build and push Docker images: bash build-and-push.sh"
    echo "2. Configure GitHub secrets: bash github-secrets.sh"
    echo "3. Trigger GitHub Actions deployment"
    echo ""
}

main "$@"
