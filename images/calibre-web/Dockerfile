# =============================================================================
# EVERGREEN HARDENED CALIBRE-WEB
# Generated from template - Version: 0.6.22
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.6.22
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D calibre 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R calibre:calibre /app /var/log/python /var/cache/python 2>/dev/null || true
USER calibre
WORKDIR /app
EXPOSE 8083

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8083/ || exit 1
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="calibre-web" \
      org.opencontainers.image.version="0.6.22" \
      org.opencontainers.image.vendor="Calibre-Web" \
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
