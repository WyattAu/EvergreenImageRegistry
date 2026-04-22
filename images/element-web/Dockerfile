# =============================================================================
# SOVEREIGN HARDENED ELEMENT-WEB
# Constraint: debian-slim - static web assets need HTTP server
# =============================================================================

ARG VERSION=1.11.12
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl -fsSL "https://github.com/element-hq/element-web/releases/download/v1.11.12/element-v1.11.12.tar.gz" -o /tmp/release.tar.gz && \
    mkdir -p /www && \
    tar -xzf /tmp/release.tar.gz -C /www --strip-components=1 && \
    rm /tmp/release.tar.gz

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx-light="1.22.*" ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser
COPY --from=downloader /www /var/www/html
RUN rm -f /etc/nginx/sites-enabled/default
RUN printf 'server {\\n    listen 8080 default_server;\\n    root /var/www/html;\\n    index index.html;\\n    location / { try_files $uri $uri/ =404; }\\n}\\n' > /etc/nginx/sites-available/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
    chown -R 65534:65534 /var/www/html /var/log/nginx /var/cache/nginx
USER 65534:65534
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/"]
CMD ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="element-web" \
      org.opencontainers.image.description="Element Web - web client for Matrix" \
      org.opencontainers.image.version="1.11.12" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/element-web" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
