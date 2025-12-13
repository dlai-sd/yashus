#!/bin/bash

# Yashus Agent Platform - Quick Start Script
# This script helps you get started quickly with the platform

set -e

echo "🚀 Yashus Agent Platform - Quick Start"
echo "======================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
echo "✅ Docker is installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
echo "✅ Docker Compose is installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys!"
    echo ""
fi

# Ask user what to do
echo ""
echo "What would you like to do?"
echo "1. Start the full platform (Backend + Frontend + Databases)"
echo "2. Start backend only"
echo "3. Start frontend only"
echo "4. Run backend tests"
echo "5. Stop all services"
echo "6. View logs"
echo "7. Clean up (remove containers and volumes)"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo "🚀 Starting full platform..."
        docker-compose up -d
        echo ""
        echo "✅ Platform started successfully!"
        echo ""
        echo "🌐 Access points:"
        echo "   - Frontend:     http://localhost:4200"
        echo "   - Backend API:  http://localhost:8000"
        echo "   - API Docs:     http://localhost:8000/docs"
        echo "   - PostgreSQL:   localhost:5432"
        echo "   - Redis:        localhost:6379"
        echo ""
        echo "📊 View logs with: docker-compose logs -f"
        echo "🛑 Stop services with: docker-compose down"
        ;;
    
    2)
        echo "🚀 Starting backend only..."
        docker-compose up -d postgres redis backend
        echo ""
        echo "✅ Backend started!"
        echo "   - API:      http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        ;;
    
    3)
        echo "🚀 Starting frontend only..."
        docker-compose up -d frontend
        echo ""
        echo "✅ Frontend started!"
        echo "   - Frontend: http://localhost:4200"
        ;;
    
    4)
        echo "🧪 Running backend tests..."
        cd backend
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        source venv/bin/activate
        pip install -q -r requirements.txt
        pytest tests/ -v --cov=app
        deactivate
        cd ..
        ;;
    
    5)
        echo "🛑 Stopping all services..."
        docker-compose down
        echo "✅ All services stopped"
        ;;
    
    6)
        echo "📊 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    
    7)
        echo "🧹 Cleaning up..."
        read -p "This will remove all containers and volumes. Are you sure? (y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            docker-compose down -v
            echo "✅ Cleanup complete"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Thank you for using Yashus Agent Platform! 🎉"
