# =============================================================================
# EVERGREEN HARDENED POWERDNS
# Generated from template - Version: 4.9.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.9.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/pdns /var/cache/pdns && chown -R appuser:appuser /app /var/log/pdns /var/cache/pdns 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 53 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["pdns"]
LABEL org.opencontainers.image.title="powerdns" \
      org.opencontainers.image.version="4.9.1" \
      org.opencontainers.image.vendor="PowerDNS" \
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
