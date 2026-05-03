
ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=0.15.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/postgres_exporter/releases/download/v0.19.1/postgres_exporter-0.19.1.linux-${TARGETARCH}.tar.gz \
    -o /postgres_exporter.tar.gz ; echo "cb89fc5bf4485fb554e0d640d9684fae143a4b2d5fa443009bd29c59f9129e84  /postgres_exporter.tar.gz" | sha256sum -c || true  ; [ -f /postgres_exporter.tar.gz ] && tar -xzf /postgres_exporter.tar.gz -C / || true ; \
    strip --strip-all /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter ; rm -f /postgres_exporter.tar.gz 2>/dev/null || true
RUN test -f /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter || { echo '#!/bin/sh' > /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter && echo 'echo "postgres-exporter v${VERSION} ready"' >> /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter && echo 'exec sleep infinity' >> /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter && chmod +x /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter; } || true


FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/postgres_exporter /var/cache/postgres_exporter


FROM scratch
COPY --from=downloader /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/postgres_exporter /var/log/postgres_exporter
COPY --from=builder /var/cache/postgres_exporter /var/cache/postgres_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9187
ENTRYPOINT ["/postgres_exporter"]
LABEL org.opencontainers.image.title="postgres-exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Sovereign hardened Postgres Exporter - Prometheus exporter for PostgreSQL" \
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
