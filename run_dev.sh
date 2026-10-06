#!/bin/bash

echo "Starting development server..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
fi

# Create directories
mkdir -p ./logs
mkdir -p ./storage/images
mkdir -p ./storage/videos

# Start with docker-compose
echo "Starting Docker services..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 5

echo ""
echo "=== Services Started ==="
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Redis: localhost:6379"
echo "PostgreSQL: localhost:5432"
echo ""
echo "View logs: docker-compose logs -f api"
echo "Stop services: docker-compose down"
