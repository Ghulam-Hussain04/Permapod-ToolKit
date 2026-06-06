#!/bin/sh
set -e

echo "[entrypoint] Starting nginx..."
exec nginx -g "daemon off;"
