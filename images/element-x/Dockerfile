# =============================================================================
# SOVEREIGN HARDENED ELEMENT-X
# Constraint: debian-slim - static web assets need HTTP server
# =============================================================================

ARG VERSION=1.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl -fsSL "https://github.com/element-hq/element-x/releases/download/v1.5.0/element-x-v1.5.0.tar.gz" -o /tmp/release.tar.gz && \
    mkdir -p /www && \
    tar -xzf /tmp/release.tar.gz -C /www --strip-components=1 && \
    rm /tmp/release.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ca-certificates
RUN groupadd -r -g 65532 appuser && useradd -r -u 65532 -g appuser -d /app -s /usr/sbin/nologin appuser
COPY --from=downloader /www /var/www/html
RUN rm -f /etc/nginx/sites-enabled/default
RUN printf 'server {\\n    listen 8080 default_server;\\n    root /var/www/html;\\n    index index.html;\\n    location / { try_files $uri $uri/ =404; }\\n}\\n' > /etc/nginx/sites-available/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx
USER 65532:65532
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="element-x" \
      org.opencontainers.image.description="Element X - next-gen Matrix client" \
      org.opencontainers.image.version="1.5.0" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/element-x" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM