# =============================================================================
# SOVEREIGN HARDENED N8N
# Generated from template - Version: 1.41.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.41.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache nodejs npm ca-certificates || true
RUN adduser -u 65532 -D node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 5678
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="n8n" \
      org.opencontainers.image.version="1.41.0" \
      org.opencontainers.image.vendor="n8n" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM