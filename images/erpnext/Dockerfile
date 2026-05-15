# =============================================================================
# EVERGREEN HARDENED ERPNEXT
# Generated from template - Version: 15.11.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=15.11.0
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D erpnext 2>/dev/null || true && \
    mkdir -p /app /var/log/erpnext /var/cache/erpnext && chown -R erpnext:erpnext /app /var/log/erpnext /var/cache/erpnext 2>/dev/null || true
USER erpnext
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8000/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="erpnext" \
      org.opencontainers.image.description="erpnext container image" \
      org.opencontainers.image.version="15.11.0" \
      org.opencontainers.image.vendor="ERPNext" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/frappe/erpnext"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
