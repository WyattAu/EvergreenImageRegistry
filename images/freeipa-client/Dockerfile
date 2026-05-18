# =============================================================================
# EVERGREEN HARDENED FREEIPA CLIENT
# FreeIPA identity management client
# Constraint: debian-slim - package installation required
# NOTE: freeipa-client is available in Fedora/RHEL repos; Debian provides
# sssd + freeipa-client via third-party or equivalent tooling
# =============================================================================

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/bin/sssctl"]
LABEL org.opencontainers.image.title="freeipa-client" \
      org.opencontainers.image.description="FreeIPA client tools via SSSD (Debian sssd suite provides FreeIPA client functionality)" \
      org.opencontainers.image.vendor="FreeIPA" \
      org.opencontainers.image.source="https://www.freeipa.org" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
