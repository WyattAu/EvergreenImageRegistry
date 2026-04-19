# =============================================================================
# SOVEREIGN HARDENED DRAGONFLY
# Generated from template - Version: 1.21.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends dragonfly ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' dragonfly 2>/dev/null || true
RUN mkdir -p /app /var/log/dragonfly /var/cache/dragonfly && chown -R dragonfly:dragonfly /app /var/log/dragonfly /var/cache/dragonfly 2>/dev/null || true
USER dragonfly:dragonfly
WORKDIR /app
EXPOSE 6379 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ADMIN ping
ENTRYPOINT ["dragonfly"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
