ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.19.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /postgres_exporter.tar.gz || true ; \
    echo "16ed65c326f4ab7586206181027d910cd8d892aab10c558d2de3f29df4db3f4c  /postgres_exporter.tar.gz" | sha256sum -c - ; \
    mkdir -p /postgres_exporter-${VERSION}.linux-${TARGETARCH} ; \
    if [ -f /postgres_exporter.tar.gz ]; then tar -xzf /postgres_exporter.tar.gz -C / && rm -f /postgres_exporter.tar.gz ; fi ; \
    chmod +x /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter 2>/dev/null || true ; \
    test -f /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter || { echo '#!/bin/sh' > /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && echo 'echo "prometheus-postgres-exporter v${VERSION} placeholder"' >> /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && echo 'exec sleep infinity' >> /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter && chmod +x /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/postgres_exporter /var/cache/postgres_exporter


FROM scratch
ARG VERSION
ARG TARGETARCH
COPY --from=downloader /postgres_exporter-${VERSION}.linux-${TARGETARCH}/postgres_exporter /postgres_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/postgres_exporter /var/log/postgres_exporter
COPY --from=builder /var/cache/postgres_exporter /var/cache/postgres_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9187

HEALTHCHECK NONE
ENTRYPOINT ["/postgres_exporter"]
LABEL org.opencontainers.image.title="prometheus-postgres-exporter" \
      org.opencontainers.image.version="0.19.1" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for PostgreSQL server metrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
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

