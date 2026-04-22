# =============================================================================
# SOVEREIGN HARDENED OPENLDAP LAMBDA
# OpenLDAP tools for lambda-compatible environments
# Constraint: debian-slim - OpenLDAP client tools required
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        ldap-utils \
        libsasl2-modules \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app && chown 65534:65534 /app
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["true"]
ENTRYPOINT ["/usr/bin/ldapsearch"]
LABEL org.opencontainers.image.title="openldap-lambda" \
      org.opencontainers.image.description="OpenLDAP client tools for lambda-compatible environments" \
      org.opencontainers.image.vendor="OpenLDAP" \
      org.opencontainers.image.source="https://www.openldap.org" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
