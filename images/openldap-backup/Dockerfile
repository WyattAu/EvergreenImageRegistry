# =============================================================================
# EVERGREEN HARDENED OPENLDAP BACKUP
# OpenLDAP backup tool using slapcat
# Constraint: debian-slim - slapcat backup tool required
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates coreutils || true && \
    mkdir -p /app /backup ; \
    chown -R 65532:65532 /app /backup
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/sbin/slapcat"]
CMD ["-l", "/backup/ldap-backup.ldif"]
LABEL org.opencontainers.image.title="openldap-backup" \
      org.opencontainers.image.description="OpenLDAP backup using slapcat" \
      org.opencontainers.image.vendor="OpenLDAP" \
      org.opencontainers.image.source="https://www.openldap.org" \
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
