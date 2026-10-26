#!/usr/bin/env sh
set -eu

ENV_FILE="${1:-.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing deployment environment file: $ENV_FILE" >&2
  exit 1
fi

echo "Pulling the requested versioned images..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" pull
echo "Starting the release..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --remove-orphans --wait
echo "Current service state:"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
