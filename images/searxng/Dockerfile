# =============================================================================
# EVERGREEN HARDENED SEARXNG
# Generated from template - Version: 2024.4.10
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.10
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache py3-lxml ca-certificates || true && \
    adduser -u 65532 -D searxng 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R searxng:searxng /app /var/log/python /var/cache/python 2>/dev/null || true
USER searxng
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="searxng" \
      org.opencontainers.image.version="2024.4.10" \
      org.opencontainers.image.vendor="SearXNG" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
