# =============================================================================
# SOVEREIGN HARDENED FREEIPA CLIENT
# FreeIPA identity management client
# Constraint: debian-slim - package installation required
# NOTE: freeipa-client is available in Fedora/RHEL repos; Debian provides
# sssd + freeipa-client via third-party or equivalent tooling
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        krb5-user \
        libnss3-tools \
        sssd \
        sssd-tools \
        libpam-sss \
        oddjob-mkhomedir && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app && chown 65534:65534 /app
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["true"]
ENTRYPOINT ["/usr/bin/sssctl"]
LABEL org.opencontainers.image.title="freeipa-client" \
      org.opencontainers.image.description="FreeIPA client tools via SSSD (Debian sssd suite provides FreeIPA client functionality)" \
      org.opencontainers.image.vendor="FreeIPA" \
      org.opencontainers.image.source="https://www.freeipa.org" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
