# =============================================================================
# SOVEREIGN HARDENED TYPESENSE-JS
# Generated from template - Version: 20
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=20
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache nodejs npm ca-certificates
RUN useradd -m -u 65532 -g '' node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 8108
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="typesense-js" \
      org.opencontainers.image.version="20" \
      org.opencontainers.image.vendor="Typesense" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM