# =============================================================================
# EVERGREEN HARDENED NEWSBOAT
# Generated from template - Version: 2.30
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.30
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D newsboat 2>/dev/null || true && \
    mkdir -p /app /var/log/newsboat /var/cache/newsboat && chown -R newsboat:newsboat /app /var/log/newsboat /var/cache/newsboat 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["newsboat"]
LABEL org.opencontainers.image.title="newsboat" \
      org.opencontainers.image.description="newsboat container image" \
      org.opencontainers.image.version="2.30" \
      org.opencontainers.image.vendor="Newsboat" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/newsboat/newsboat"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
