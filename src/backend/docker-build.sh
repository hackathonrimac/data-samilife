#!/bin/bash
# Script para construir la imagen Docker de la Healthcare API

echo "======================================"
echo "Building Healthcare API Docker Image"
echo "======================================"

# Construir la imagen
docker build -t healthcare-api:latest .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker run -p 8000:8000 --env-file .env healthcare-api:latest"
    echo ""
    echo "Or use docker-compose:"
    echo "  docker-compose up"
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
