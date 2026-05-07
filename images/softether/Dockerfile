# =============================================================================
# EVERGREEN HARDENED SOFTETHER
# Generated from template - Version: 4.38-9770
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.38-9770
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache build-base ca-certificates || true && \
    adduser -u 65532 -D appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/vpnserver /var/cache/vpnserver && chown -R appuser:appuser /app /var/log/vpnserver /var/cache/vpnserver 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 443 992 1194 500 4500 5555

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:443/ || exit 1
ENTRYPOINT ["vpnserver"]
LABEL org.opencontainers.image.title="softether" \
      org.opencontainers.image.description="softether container image" \
      org.opencontainers.image.version="4.38-9770" \
      org.opencontainers.image.vendor="SoftEther" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/SoftEtherVPN/SoftEtherVPN"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
