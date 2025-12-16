#!/bin/bash
# build-and-push.sh
# Build Docker images and push to Azure Container Registry

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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUTS_FILE="${SCRIPT_DIR}/deployment-outputs.json"

if [ ! -f "$OUTPUTS_FILE" ]; then
    log_error "deployment-outputs.json not found. Run deploy-to-azure.sh first."
    exit 1
fi

# Extract registry details
REGISTRY_URL=$(jq -r '.registryLoginServer.value' "$OUTPUTS_FILE")
REGISTRY_USERNAME=$(jq -r '.registryUsername.value' "$OUTPUTS_FILE")
REGISTRY_PASSWORD=$(jq -r '.registryPassword.value' "$OUTPUTS_FILE")

log_info "Building and pushing images to: $REGISTRY_URL"

# Login to ACR
log_info "Logging into Azure Container Registry..."
echo "$REGISTRY_PASSWORD" | docker login "$REGISTRY_URL" -u "$REGISTRY_USERNAME" --password-stdin
log_success "Logged in to ACR"

cd "$PROJECT_ROOT"

# Build and push backend
log_info "Building backend image..."
docker build -t "$REGISTRY_URL/the-hunter-api:latest" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -f TheHunter/backend/Dockerfile \
    TheHunter/backend || {
    log_error "Failed to build backend image"
    exit 1
}

log_info "Pushing backend image..."
docker push "$REGISTRY_URL/the-hunter-api:latest" || {
    log_error "Failed to push backend image"
    exit 1
}
log_success "Backend image pushed"

# Build and push frontend
log_info "Building frontend image..."
docker build -t "$REGISTRY_URL/the-hunter-frontend:latest" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -f TheHunter/frontend/Dockerfile \
    TheHunter/frontend || {
    log_error "Failed to build frontend image"
    exit 1
}

log_info "Pushing frontend image..."
docker push "$REGISTRY_URL/the-hunter-frontend:latest" || {
    log_error "Failed to push frontend image"
    exit 1
}
log_success "Frontend image pushed"

echo ""
log_success "All images built and pushed successfully! 🎉"
echo ""
echo "Next: Configure GitHub secrets with:"
echo "  bash ${SCRIPT_DIR}/github-secrets.sh"
