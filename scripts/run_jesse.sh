#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="$REPO_ROOT/Jesse/tradecore-jesse"
DOCKER_DIR="$PROJECT_DIR/docker"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_BIN="docker-compose"
else
  echo "Docker Compose is required (install docker compose plugin or docker-compose binary)" >&2
  exit 1
fi

if [[ ! -d "$DOCKER_DIR" ]]; then
  echo "Jesse project not found at $PROJECT_DIR" >&2
  exit 1
fi

command=${1:-up}
case "$command" in
  up)
    if [[ ! -f "$PROJECT_DIR/.env" ]]; then
      cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
      echo "Created $PROJECT_DIR/.env from template"
    fi
    cd "$DOCKER_DIR"
    $COMPOSE_BIN up -d
    DASH_PWD=$(grep '^PASSWORD=' "$PROJECT_DIR/.env" | cut -d= -f2-)
    echo "Jesse dashboard running at http://localhost:9000 (password: ${DASH_PWD:-<unset>})"
    ;;
  down)
    cd "$DOCKER_DIR"
    $COMPOSE_BIN down
    echo "Jesse stack stopped"
    ;;
  logs)
    cd "$DOCKER_DIR"
    $COMPOSE_BIN logs -f
    ;;
  *)
    echo "Usage: $0 [up|down|logs]" >&2
    exit 1
    ;;
 esac
