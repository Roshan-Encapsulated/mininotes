#!/bin/bash

echo "Pulling latest image..."
docker pull roshaaaaan/mininotes

echo "Stopping old containers..."
docker-compose down

echo "Starting updated containers..."
docker-compose up -d

echo "Deployment done 🚀"