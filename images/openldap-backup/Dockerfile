# =============================================================================
# SOVEREIGN HARDENED OPENLDAP BACKUP
# OpenLDAP backup tool using slapcat
# Constraint: debian-slim - slapcat backup tool required
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates coreutils || true
RUN mkdir -p /app /backup ; \
    chown -R 65532:65532 /app /backup
USER 65532:65532
WORKDIR /app
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
