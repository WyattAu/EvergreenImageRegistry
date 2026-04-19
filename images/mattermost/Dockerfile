# =============================================================================
# SOVEREIGN HARDENED MATTERMOST
# Generated from template - Version: 10.1.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends mattermost ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' mattermost 2>/dev/null || true
RUN mkdir -p /app /var/log/mattermost /var/cache/mattermost && chown -R mattermost:mattermost /app /var/log/mattermost /var/cache/mattermost 2>/dev/null || true
USER mattermost
WORKDIR /app
EXPOSE 8065
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mattermost curl -s localhost:8065/api/v4/system/ping
ENTRYPOINT ["mattermost"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.version="10.1.0" \
      org.opencontainers.image.vendor="Mattermost" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
