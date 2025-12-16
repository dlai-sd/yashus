#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 The Hunter - Local Setup${NC}"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f "./common/.env" ]; then
    echo -e "\n${YELLOW}Creating .env file...${NC}"
    cp ./common/.env.example ./common/.env
    echo -e "${GREEN}✅ .env file created from template${NC}"
fi

# Build and start services
echo -e "\n${YELLOW}Building Docker images...${NC}"
docker-compose -f ./TheHunter/docker-compose.yml build

echo -e "\n${YELLOW}Starting services...${NC}"
docker-compose -f ./TheHunter/docker-compose.yml up -d

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Check services
echo -e "\n${YELLOW}Checking service health...${NC}"

if curl -f http://localhost:8000/api/v1/calculator/health &> /dev/null; then
    echo -e "${GREEN}✅ API is healthy${NC}"
else
    echo -e "${RED}❌ API is not responding${NC}"
fi

echo -e "\n${GREEN}🎉 Setup complete!${NC}"
echo -e "\n${YELLOW}Services running:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:4200${NC}"
echo -e "  API: ${GREEN}http://localhost:8000${NC}"
echo -e "  Database: ${GREEN}localhost:5432${NC}"

echo -e "\n${YELLOW}Useful commands:${NC}"
echo -e "  View logs: docker-compose -f ./TheHunter/docker-compose.yml logs -f"
echo -e "  Stop services: docker-compose -f ./TheHunter/docker-compose.yml down"
echo -e "  Run tests: docker-compose -f ./TheHunter/docker-compose.yml exec api pytest tests/"
