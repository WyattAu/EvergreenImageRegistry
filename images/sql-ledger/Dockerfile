ARG VERSION=2.8.38
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache perl apache2 ca-certificates curl || true
RUN mkdir -p /var/www/sql-ledger /var/log/sql-ledger \ ; \
    chown -R 65532:65532 /var/www/sql-ledger /var/log/sql-ledgerUSER 65532:65532
WORKDIR /var/www/sql-ledger
EXPOSE 80
ENTRYPOINT ["httpd", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="sql-ledger" \
      org.opencontainers.image.version="2.8.38" \
      org.opencontainers.image.vendor="SQL-Ledger" \
      org.opencontainers.image.source="https://www.ledgersmb.org/" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM