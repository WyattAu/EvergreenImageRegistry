# =============================================================================
# EVERGREEN HARDENED HOMEASSISTANT
# Generated from template - Version: 2024.4.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D homeassistant 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R homeassistant:homeassistant /app /var/log/python /var/cache/python 2>/dev/null || true
USER homeassistant
WORKDIR /app
EXPOSE 8123

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8123/ || exit 1
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="homeassistant" \
      org.opencontainers.image.version="2024.4.2" \
      org.opencontainers.image.vendor="Home Assistant" \
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
