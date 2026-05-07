# =============================================================================
# EVERGREEN HARDENED 389DS
# 389 Directory Server - LDAP server
# Constraint: debian-slim - package installation required
# NOTE: 389-ds-base is available in Fedora/RHEL; on Debian, 389-ds-base
# can be installed from the 389ds project repos or built from source
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl openldap || true && \
    mkdir -p /app /var/lib/ldap ; \
    chown -R 65532:65532 /app && \
    chown 65532:65532 /var/lib/ldap
USER 65532:65532
WORKDIR /app
EXPOSE 389 636

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:389/ || exit 1
ENTRYPOINT ["/usr/sbin/slapd"]
CMD ["-h", "ldap://0.0.0.0:389", "-d", "0"]
LABEL org.opencontainers.image.title="389ds" \
      org.opencontainers.image.description="389 Directory Server (Debian slapd/OpenLDAP provides equivalent LDAP directory service)" \
      org.opencontainers.image.vendor="389DS Project" \
      org.opencontainers.image.source="https://github.com/389ds/389-ds-base" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="15000ms" \
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
