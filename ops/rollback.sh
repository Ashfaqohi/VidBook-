#!/usr/bin/env sh
set -eu

TARGET_VERSION="${1:-}"
ENV_FILE="${2:-.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

if [ -z "$TARGET_VERSION" ]; then
  echo "Usage: $0 <known-good-version> [env-file]" >&2
  exit 1
fi
if [ ! -f "$ENV_FILE" ]; then
  echo "Missing deployment environment file: $ENV_FILE" >&2
  exit 1
fi

echo "Rolling back to version $TARGET_VERSION..."
VIDBOOK_VERSION="$TARGET_VERSION" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" pull
VIDBOOK_VERSION="$TARGET_VERSION" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --remove-orphans --wait
echo "Rollback service state:"
VIDBOOK_VERSION="$TARGET_VERSION" docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
