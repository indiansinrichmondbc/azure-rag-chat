#!/bin/bash

# Exit on error
set -e

echo "Starting local deployment..."

# Install PostgreSQL client and libpq-dev
sudo apt-get update && sudo apt-get install -y postgresql-client libpq-dev

# Create local directories if they don't exist
mkdir -p ./temp_docs

# Build the Docker image
echo "Building Docker image..."
docker build -t rag-app:local .

# Stop and remove existing container if it exists
echo "Cleaning up existing container..."
docker rm -f rag-app 2>/dev/null || true

# Run the container
echo "Starting container..."
docker run -d \
    --name rag-app \
    --env-file .env \
    -p 8501:8501 \
    -v "$(pwd)/temp_docs:/app/temp_docs" \
    rag-app:local

# Wait for the application to start
echo "Waiting for application to start..."
sleep 5

# Check container status
CONTAINER_STATUS=$(docker ps -f name=rag-app --format "{{.Status}}")
if [[ $CONTAINER_STATUS == *"Up"* ]]; then
    echo "Application is running!"
    echo "Access the application at: http://localhost:8501"
    echo "View container logs with: docker logs rag-app"
else
    echo "Container failed to start. Checking logs..."
    docker logs rag-app
    exit 1
fi
