# =============================================================================
# EVERGREEN HARDENED 389DS
# 389 Directory Server - LDAP server
# Constraint: debian-slim - package installation required
# NOTE: 389-ds-base is available in Fedora/RHEL; on Debian, 389-ds-base
# can be installed from the 389ds project repos or built from source
# =============================================================================

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates curl openldap && \
    mkdir -p /app /var/lib/ldap ; \
    chown -R 65532:65532 /app && \
    chown 65532:65532 /var/lib/ldap
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 389 636

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:389"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/sbin/slapd", "--", "-h", "ldap://0.0.0.0:389", "-d", "0"]
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
