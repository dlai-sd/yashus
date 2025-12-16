#!/bin/bash
# setup-from-config.sh
# Setup local development environment from devconfig.yaml
# Generates docker-compose, builds services with change detection, and starts containers

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEVCONFIG="${PROJECT_ROOT}/devconfig.yaml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Helper functions
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

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        missing_tools+=("docker-compose")
    fi
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        echo "Please install the missing tools and try again."
        exit 1
    fi
    
    if [ ! -f "$DEVCONFIG" ]; then
        log_error "devconfig.yaml not found at $DEVCONFIG"
        exit 1
    fi
    
    log_success "Prerequisites satisfied"
}

# Generate docker-compose from config
generate_compose() {
    log_info "Generating docker-compose.yml from devconfig.yaml..."
    
    cd "$PROJECT_ROOT"
    
    python3 common/scripts/generate-docker-compose.py local
    
    if [ $? -eq 0 ]; then
        log_success "docker-compose.yml generated"
    else
        log_error "Failed to generate docker-compose.yml"
        return 1
    fi
}

# Build services with change detection
build_services() {
    log_info "Building services..."
    
    cd "$PROJECT_ROOT"
    
    bash common/scripts/build-orchestrator.sh build local false
    
    if [ $? -eq 0 ]; then
        log_success "Services built successfully"
    else
        log_error "Service build failed"
        return 1
    fi
}

# Start services
start_services() {
    log_info "Starting services..."
    
    cd "$PROJECT_ROOT/TheHunter"
    
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        log_success "Services started"
    else
        log_error "Failed to start services"
        return 1
    fi
}

# Wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy..."
    
    local max_attempts=30
    local attempt=0
    
    # Database
    log_info "Checking database..."
    while [ $attempt -lt $max_attempts ]; do
        if docker exec thehunter-database-1 pg_isready -U hunter -d the_hunter &>/dev/null; then
            log_success "Database is healthy"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        log_error "Database failed to start"
        return 1
    fi
    
    # Backend
    attempt=0
    log_info "Checking backend API..."
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8000/api/v1/calculator/health &>/dev/null; then
            log_success "Backend API is healthy"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        log_error "Backend API failed to start"
        return 1
    fi
    
    # Frontend
    attempt=0
    log_info "Checking frontend..."
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:4200 &>/dev/null; then
            log_success "Frontend is healthy"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        log_warn "Frontend not yet ready, but continuing"
    fi
}

# Show summary
show_summary() {
    echo ""
    log_success "Environment setup completed! 🎉"
    echo ""
    echo "Services are running:"
    echo "  📱 Frontend:  http://localhost:4200"
    echo "  🔧 API:       http://localhost:8000"
    echo "  📊 API Docs:  http://localhost:8000/docs"
    echo "  💾 Database:  localhost:5432"
    echo ""
    echo "Useful commands:"
    echo "  View logs:           docker-compose logs -f"
    echo "  Stop services:       docker-compose down"
    echo "  Run tests:           bash common/scripts/run-tests.sh"
    echo "  Check build status:  bash common/scripts/build-orchestrator.sh status"
    echo ""
}

# Main
main() {
    echo "🚀 Starting The Hunter development environment setup..."
    echo ""
    
    check_prerequisites
    
    generate_compose || exit 1
    
    build_services || exit 1
    
    start_services || exit 1
    
    wait_for_services || exit 1
    
    show_summary
}

main "$@"
