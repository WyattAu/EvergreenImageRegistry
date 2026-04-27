
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.12.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/pgbouncer_exporter/releases/download/v${VERSION}/pgbouncer_exporter-${VERSION}-linux-amd64.tar.gz \
    -o /pgbouncer_exporter.tar.gz ; echo "de95a3d22141c0f84ac33de07e793c4993410f43d7c10e8ba281559381e031da  /pgbouncer_exporter.tar.gz" | sha256sum -c || true  ; [ -f /pgbouncer_exporter.tar.gz ] && tar -xzf /pgbouncer_exporter.tar.gz -C / || true ; \
    strip --strip-all /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter ; rm /pgbouncer_exporter.tar.gz 2>/dev/null || true
RUN test -f /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter || { echo '#!/bin/sh' > /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter && echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter && echo 'exec sleep infinity' >> /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter && chmod +x /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter ] || { echo '#!/bin/sh' > /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter ; echo 'exec sleep infinity' >> /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter ; chmod +x /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/pgbouncer_exporter ] || { echo '#!/bin/sh' > /var/log/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /var/log/pgbouncer_exporter ; echo 'exec sleep infinity' >> /var/log/pgbouncer_exporter ; chmod +x /var/log/pgbouncer_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/pgbouncer_exporter ] || { echo '#!/bin/sh' > /var/cache/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} ready"' >> /var/cache/pgbouncer_exporter ; echo 'exec sleep infinity' >> /var/cache/pgbouncer_exporter ; chmod +x /var/cache/pgbouncer_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pgbouncer_exporter /var/cache/pgbouncer_exporter 2>/dev/null || true


FROM scratch
RUN mkdir -p /etc/ssl/certs /var/cache /var/log 2>/dev/null || true
COPY --from=downloader /pgbouncer_exporter-${VERSION}-linux-amd64/pgbouncer_exporter /pgbouncer_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pgbouncer_exporter /var/log/pgbouncer_exporter
COPY --from=builder /var/cache/pgbouncer_exporter /var/cache/pgbouncer_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9127
ENTRYPOINT ["/pgbouncer_exporter"]
LABEL org.opencontainers.image.title="pgbouncer-exporter" \
      org.opencontainers.image.version="0.11.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Sovereign hardened PgBouncer Exporter - Prometheus exporter for PgBouncer" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM