# =============================================================================
# EVERGREEN HARDENED TRANSMISSION
# Generated from template - Version: 4.0.6
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.6
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D transmission 2>/dev/null || true
RUN mkdir -p /app /var/log/transmission-daemon /var/cache/transmission-daemon && chown -R transmission:transmission /app /var/log/transmission-daemon /var/cache/transmission-daemon 2>/dev/null || true
USER transmission
WORKDIR /app
EXPOSE 9091

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9091/ || exit 1
ENTRYPOINT ["transmission-daemon"]
LABEL org.opencontainers.image.title="transmission" \
      org.opencontainers.image.version="4.0.6" \
      org.opencontainers.image.vendor="Transmission" \
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
