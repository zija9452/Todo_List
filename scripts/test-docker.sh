#!/bin/bash

echo "Starting Full-Stack Todo Application with Docker..."

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi

echo "Building and starting containers..."
docker-compose up --build -d

echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking if containers are running..."
docker-compose ps

echo ""
echo "Application is now running:"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the application, run: docker-compose down"

# Optional: Test the API endpoint
echo ""
echo "Testing backend health endpoint..."
sleep 5
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Backend is responding"
    curl -s http://localhost:8000/health | python -m json.tool
else
    echo "✗ Backend is not responding"
fi

echo ""
echo "Application setup complete!"