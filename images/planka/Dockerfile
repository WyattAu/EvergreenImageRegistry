# =============================================================================
# EVERGREEN HARDENED PLANKA
# Generated from template - Version: 1.17.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.17.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache nodejs npm ca-certificates 
RUN adduser -u 65532 -D planka 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R planka:planka /app /var/log/node /var/cache/node 2>/dev/null || true
USER planka
WORKDIR /app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3000/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="planka" \
      org.opencontainers.image.version="1.17.0" \
      org.opencontainers.image.vendor="Planka" \
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
