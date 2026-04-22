# =============================================================================
# SOVEREIGN HARDENED MYTHTV
# Generated from template - Version: 34.0
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=34.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    mythtv-backend mythtv-frontend mythtv-database ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' mythtv 2>/dev/null || true
RUN mkdir -p /app /var/log/mythtv /var/cache/mythtv && chown -R mythtv:mythtv /app /var/log/mythtv /var/cache/mythtv 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 6543
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:6543/ || exit 1
ENTRYPOINT ["mythbackend"]
LABEL org.opencontainers.image.title="mythtv" \
      org.opencontainers.image.version="34.0" \
      org.opencontainers.image.vendor="MythTV" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
