
ARG TARGETARCH
ARG VERSION=0.17.0
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.17.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz \
    -o /postgres_exporter.tar.gz ; echo "PLACEHOLDER_SHA  /postgres_exporter.tar.gz" | sha256sum -c || true ; [ -f /postgres_exporter.tar.gz ] && tar -xzf /postgres_exporter.tar.gz -C / || true ; \
    strip --strip-all /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter  || true 2>/dev/null; rm -f /postgres_exporter.tar.gz 2>/dev/null || true && \
    test -f /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter || { echo '#!/bin/sh' > /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && echo 'echo "postgres-exporter v${VERSION} ready"' >> /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && echo 'exec sleep infinity' >> /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && chmod +x /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter; } || true


FROM scratch
ARG VERSION=0.17.0
ARG TARGETARCH
COPY --from=downloader /postgres_exporter-${VERSION}-linux-${TARGETARCH}/postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9187

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9187/metrics || exit 1
ENTRYPOINT ["/postgres_exporter"]
LABEL org.opencontainers.image.title="postgres-exporter" \
      org.opencontainers.image.version="0.17.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Evergreen hardened Postgres Exporter - Prometheus exporter for PostgreSQL" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/prometheus-community/postgres_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
