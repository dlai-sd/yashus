#!/bin/bash

# Run tests in Docker containers
echo "🧪 Running Tests..."

echo -e "\n📝 Backend Tests:"
docker-compose -f ./TheHunter/docker-compose.yml exec -T api pytest tests/ -v --cov=app

echo -e "\n🎨 Frontend Tests:"
docker-compose -f ./TheHunter/docker-compose.yml exec -T frontend npm run test -- --watch=false

echo -e "\n✅ Tests completed!"
