# =============================================================================
# SOVEREIGN HARDENED 389DS
# 389 Directory Server - LDAP server
# Constraint: debian-slim - package installation required
# NOTE: 389-ds-base is available in Fedora/RHEL; on Debian, 389-ds-base
# can be installed from the 389ds project repos or built from source
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl openldap
RUN mkdir -p /app /var/lib/ldap && \
    chown -R 65532:65532 /app && \
    chown openldap:openldap /var/lib/ldap
USER 65532:65532
WORKDIR /app
EXPOSE 389 636
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
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM