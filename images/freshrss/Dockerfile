# =============================================================================
# SOVEREIGN HARDENED FRESHRSS
# Generated from template - Version: 1.24.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.24.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends php83 php83-fpm php83-curl php83-mbstring php83-xml ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER www-data
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD php curl -s localhost:80/i/status
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="freshrss" \
      org.opencontainers.image.version="1.24.1" \
      org.opencontainers.image.vendor="FreshRSS" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
