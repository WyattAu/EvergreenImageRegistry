# =============================================================================
# SOVEREIGN HARDENED NGINX-CACHE
# NGINX reverse proxy with caching enabled
# Constraint: debian-slim - nginx requires dynamic libs, cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.27.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 lsb-release && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://nginx.org/keys/nginx_signing.key" | gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian bookworm nginx" > /etc/apt/sources.list.d/nginx.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx=${VERSION}-1~bookworm && \
    rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx /var/cache/nginx/proxy /var/cache/nginx/fastcgi /run && \
    chown -R 65534:65534 /app /var/log/nginx /var/cache/nginx

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libpcre3 libz1 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /usr/sbin/nginx /usr/sbin/nginx
COPY --from=downloader /etc/nginx /etc/nginx
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/cache/nginx /var/cache/nginx
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/nginx", "-v"]
ENTRYPOINT ["/usr/sbin/nginx"]
CMD ["-g", "daemon off;"]
LABEL org.opencontainers.image.title="nginx-cache" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.source="https://nginx.org" \
      org.opencontainers.image.description="NGINX reverse proxy with caching support" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
