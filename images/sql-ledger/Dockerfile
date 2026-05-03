ARG VERSION=2.8.38
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache perl apache2 ca-certificates curl || true
RUN mkdir -p /var/www/sql-ledger /var/log/sql-ledger ; 2>/dev/null || true \
    chown -R 65532:65532 /var/www/sql-ledger /var/log/sql-ledger
USER 65532:65532
WORKDIR /var/www/sql-ledger
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["httpd", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="sql-ledger" \
      org.opencontainers.image.version="2.8.38" \
      org.opencontainers.image.vendor="SQL-Ledger" \
      org.opencontainers.image.source="https://www.ledgersmb.org/" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
