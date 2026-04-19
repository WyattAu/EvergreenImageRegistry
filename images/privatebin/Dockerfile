# =============================================================================
# SOVEREIGN HARDENED PRIVATEBIN
# Generated from template - Version: 1.6.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends php83 php83-fpm php83-curl php83-mbstring ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER www-data
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD php curl -s localhost:80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="privatebin" \
      org.opencontainers.image.version="1.6.0" \
      org.opencontainers.image.vendor="PrivateBin" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
