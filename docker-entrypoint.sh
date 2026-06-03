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
if [ -z "$GROQ_API_KEY" ]; then
  echo "[entrypoint] WARNING: GROQ_API_KEY is not set."
else
  echo "[entrypoint] Injecting API key into index.html..."
fi

# Replace placeholder with real key
sed -i "s|%%GROQ_API_KEY%%|${GROQ_API_KEY}|g" "$HTML_FILE"

echo "[entrypoint] Starting nginx..."
exec nginx -g "daemon off;"
