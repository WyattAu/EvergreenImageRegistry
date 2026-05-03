# =============================================================================
# EVERGREEN HARDENED TVHEADEND
# Generated from template - Version: 4.3
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D hts 2>/dev/null || true
RUN mkdir -p /app /var/log/hts /var/cache/hts && chown -R hts:hts /app /var/log/hts /var/cache/hts 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9981

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9981/ || exit 1
ENTRYPOINT ["tvheadend"]
LABEL org.opencontainers.image.title="tvheadend" \
      org.opencontainers.image.version="4.3" \
      org.opencontainers.image.vendor="TVHeadend" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
