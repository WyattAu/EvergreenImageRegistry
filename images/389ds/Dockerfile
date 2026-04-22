# =============================================================================
# SOVEREIGN HARDENED 389DS
# 389 Directory Server - LDAP server
# Constraint: debian-slim - package installation required
# NOTE: 389-ds-base is available in Fedora/RHEL; on Debian, 389-ds-base
# can be installed from the 389ds project repos or built from source
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        openldap \
        slapd \
        ldap-utils \
        libsasl2-modules \
        cyrus-sasl2-bin && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/lib/ldap && \
    chown -R 65534:65534 /app && \
    chown openldap:openldap /var/lib/ldap
USER 65534:65534
WORKDIR /app
EXPOSE 389 636
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["ldapsearch", "-x", "-H", "ldap://localhost:389", "-b", "", "-s", "base", "(objectclass=*)"]
ENTRYPOINT ["/usr/sbin/slapd"]
CMD ["-h", "ldap://0.0.0.0:389", "-d", "0"]
LABEL org.opencontainers.image.title="389ds" \
      org.opencontainers.image.description="389 Directory Server (Debian slapd/OpenLDAP provides equivalent LDAP directory service)" \
      org.opencontainers.image.vendor="389DS Project" \
      org.opencontainers.image.source="https://github.com/389ds/389-ds-base" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
