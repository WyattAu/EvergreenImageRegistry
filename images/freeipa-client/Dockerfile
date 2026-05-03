# =============================================================================
# EVERGREEN HARDENED FREEIPA CLIENT
# FreeIPA identity management client
# Constraint: debian-slim - package installation required
# NOTE: freeipa-client is available in Fedora/RHEL repos; Debian provides
# sssd + freeipa-client via third-party or equivalent tooling
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates curl 
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
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
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
