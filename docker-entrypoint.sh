#!/bin/sh
# ─────────────────────────────────────────────────
# docker-entrypoint.sh
#
# Runs at container startup BEFORE nginx starts.
# Replaces the %%OPENROUTER_API_KEY%% placeholder
# in index.html with the real key from the
# OPENROUTER_API_KEY environment variable.
#
# This means:
#  - The key is NEVER hardcoded in source code
#  - The key is NEVER baked into the Docker image
#  - The key is injected at runtime from .env / docker-compose
# ─────────────────────────────────────────────────

set -e

HTML_FILE="/usr/share/nginx/html/index.html"

# Validate that the key is present
if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "[entrypoint] WARNING: OPENROUTER_API_KEY is not set."
  echo "[entrypoint] The app will prompt users to enter their key manually."
  API_KEY=""
else
  echo "[entrypoint] Injecting API key into index.html..."
  API_KEY="$OPENROUTER_API_KEY"
fi

# Replace placeholder with real key
sed -i "s|%%OPENROUTER_API_KEY%%|${API_KEY}|g" "$HTML_FILE"

echo "[entrypoint] Starting nginx..."
exec nginx -g "daemon off;"
