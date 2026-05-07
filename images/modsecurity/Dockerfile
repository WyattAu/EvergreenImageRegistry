# =============================================================================
# EVERGREEN HARDENED MODSECURITY
# Generated from template - Version: 2.4.59
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.59
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache apache2 ca-certificates || true && \
    adduser -u 65532 -D appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/apache2 /var/cache/apache2 && chown -R appuser:appuser /app /var/log/apache2 /var/cache/apache2 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["apache2"]
LABEL org.opencontainers.image.title="modsecurity" \
      org.opencontainers.image.description="modsecurity container image" \
      org.opencontainers.image.version="2.4.59" \
      org.opencontainers.image.vendor="OWASP" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/SpiderLabs/ModSecurity"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
