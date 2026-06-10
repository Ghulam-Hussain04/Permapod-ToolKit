# ─────────────────────────────────────────────────
# Permapod X Content Manager — Dockerfile
# ─────────────────────────────────────────────────

FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy static app files — preserve folder structure
COPY index.html       /usr/share/nginx/html/index.html
COPY src/             /usr/share/nginx/html/src/

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy and register the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080
RUN sed -i 's/\r//' /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]