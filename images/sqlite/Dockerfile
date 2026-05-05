# =============================================================================
# EVERGREEN HARDENED SQLITE
# Generated from template - Version: 3.45.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.45.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache sqlite-libs ca-certificates && \
    adduser -u 65532 -D sqlite 2>/dev/null || true && \
    mkdir -p /app /var/log/sqlite-libs /var/cache/sqlite-libs && chown -R sqlite:sqlite /app /var/log/sqlite-libs /var/cache/sqlite-libs 2>/dev/null || true
USER sqlite
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["sqlite-libs"]
LABEL org.opencontainers.image.title="sqlite" \
      org.opencontainers.image.description="sqlite container image" \
      org.opencontainers.image.version="3.45.1" \
      org.opencontainers.image.vendor="SQLite" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/sqlite/sqlite"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
