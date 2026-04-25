# =============================================================================
# SOVEREIGN HARDENED UPTIME-KUMA
# Generated from template - Version: 1.23.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.23.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache nodejs npm ca-certificates || true
RUN adduser -u 65532 -D node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 3001
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="uptime-kuma" \
      org.opencontainers.image.version="1.23.1" \
      org.opencontainers.image.vendor="Uptime Kuma" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM