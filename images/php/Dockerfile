# =============================================================================
# SOVEREIGN HARDENED PHP
# Generated from template - Version: 8.3.8
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.3.8
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    php-cli php-common ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin php 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    php-cli ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/php /var/log/php
COPY --from=builder --chown=65534:65534 /var/cache/php /var/cache/php
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD php --version
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="php" \
      org.opencontainers.image.version="8.3.8" \
      org.opencontainers.image.vendor="PHP" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
