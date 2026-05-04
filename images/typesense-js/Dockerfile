# =============================================================================
# EVERGREEN HARDENED TYPESENSE-JS
# Generated from template - Version: 20
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=20
ARG BUILD_DATE
ARG TARGETARCH


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache nodejs npm ca-certificates && \
    adduser -u 65532 -D node 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 8108

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8108/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="typesense-js" \
      org.opencontainers.image.version="20" \
      org.opencontainers.image.vendor="Typesense" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
