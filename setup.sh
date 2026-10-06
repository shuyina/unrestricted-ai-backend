#!/bin/bash

echo "=== Unrestricted AI Backend Setup ==="

# Create directories
mkdir -p ./logs
mkdir -p ./storage/images
mkdir -p ./storage/videos
mkdir -p ./storage/uploads

echo "Directories created"

# Create .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
fi

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Run: docker-compose up"
echo "3. API will be available at http://localhost:8000"
echo "4. API docs at http://localhost:8000/docs"
