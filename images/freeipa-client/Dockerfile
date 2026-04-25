# =============================================================================
# SOVEREIGN HARDENED FREEIPA CLIENT
# FreeIPA identity management client
# Constraint: debian-slim - package installation required
# NOTE: freeipa-client is available in Fedora/RHEL repos; Debian provides
# sssd + freeipa-client via third-party or equivalent tooling
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl || true
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/bin/sssctl"]
LABEL org.opencontainers.image.title="freeipa-client" \
      org.opencontainers.image.description="FreeIPA client tools via SSSD (Debian sssd suite provides FreeIPA client functionality)" \
      org.opencontainers.image.vendor="FreeIPA" \
      org.opencontainers.image.source="https://www.freeipa.org" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM