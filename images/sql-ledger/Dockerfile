ARG VERSION=2.8.38
ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        perl libdbd-pg-perl libdbi-perl libjson-perl \
        libcgi-pm-perl libapache-dbi-perl libtemplate-perl \
        apache2 libapache2-mod-perl2 ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/www/sql-ledger /var/log/sql-ledger \
    && chown -R 65534:65534 /var/www/sql-ledger /var/log/sql-ledger
USER 65534:65534
WORKDIR /var/www/sql-ledger
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:80"]
ENTRYPOINT ["httpd", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="sql-ledger" \
      org.opencontainers.image.version="2.8.38" \
      org.opencontainers.image.vendor="SQL-Ledger" \
      org.opencontainers.image.source="https://www.ledgersmb.org/" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
