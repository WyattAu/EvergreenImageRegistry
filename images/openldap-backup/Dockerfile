# =============================================================================
# SOVEREIGN HARDENED OPENLDAP BACKUP
# OpenLDAP backup tool using slapcat
# Constraint: debian-slim - slapcat backup tool required
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        slapd \
        ldap-utils \
        coreutils && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /backup && \
    chown -R 65534:65534 /app /backup
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["true"]
ENTRYPOINT ["/usr/sbin/slapcat"]
CMD ["-l", "/backup/ldap-backup.ldif"]
LABEL org.opencontainers.image.title="openldap-backup" \
      org.opencontainers.image.description="OpenLDAP backup using slapcat" \
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
