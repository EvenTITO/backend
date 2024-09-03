#!/bin/bash
docker compose -f docker-compose-dev.yaml down

NETWORK_NAME="eventito-dev-network"

if docker network ls --format '{{.Name}}' | grep -wq "$NETWORK_NAME"; then
    echo "Removing network '$NETWORK_NAME'..."
    docker network rm "$NETWORK_NAME"
fi
