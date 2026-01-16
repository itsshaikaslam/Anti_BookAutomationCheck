#!/bin/bash
set -e

echo "Running health check for eBook System..."

# 1. Check if containers are running
if [ "$(docker ps -q -f name=ebook-db)" ]; then
    echo "Postgres is UP"
else
    echo "Postgres is DOWN"
    exit 1
fi

if [ "$(docker ps -q -f name=ebook-redis)" ]; then
    echo "Redis is UP"
else
    echo "Redis is DOWN"
    exit 1
fi

if [ "$(docker ps -q -f name=ebook-minio)" ]; then
    echo "MinIO is UP"
else
    echo "MinIO is DOWN"
    exit 1
fi

# 2. Check API health
# Note: This might need a few seconds if just started
MAX_RETRIES=5
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
    status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
    if [ $status_code -eq 200 ]; then
        echo "Backend API is UP"
        break
    else
        echo "Waiting for API... ($status_code)"
        COUNT=$((COUNT+1))
        sleep 5
    fi
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Backend API failed to respond after $MAX_RETRIES attempts"
    exit 1
fi

echo "All core services verified!"
