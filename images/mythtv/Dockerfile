# =============================================================================
# SOVEREIGN HARDENED MYTHTV
# Generated from template - Version: 34.0
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=34.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    mythtv-backend mythtv-frontend mythtv-database ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' mythtv 2>/dev/null || true
RUN mkdir -p /app /var/log/mythtv /var/cache/mythtv && chown -R mythtv:mythtv /app /var/log/mythtv /var/cache/mythtv 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6543
ENTRYPOINT ["mythbackend"]
LABEL org.opencontainers.image.title="mythtv" \
      org.opencontainers.image.version="34.0" \
      org.opencontainers.image.vendor="MythTV" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM