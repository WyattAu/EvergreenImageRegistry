# =============================================================================
# EVERGREEN HARDENED TYPESENSE-JS
# Generated from template - Version: 20
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=20
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache nodejs-20 npm ca-certificates && \
    adduser -u 65532 -D node 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 8108

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8108/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="typesense-js" \
      org.opencontainers.image.description="typesense-js container image" \
      org.opencontainers.image.version="20" \
      org.opencontainers.image.vendor="Typesense" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/typesense/typesense"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
