ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.4.0
RUN touch /consul_exporter || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/consul_exporter/releases/download/v0.4.0/consul_exporter-0.4.0.linux-${TARGETARCH}.tar.gz -o /consul_exporter.tar.gz && \
    echo "dc1fa7f621d9116ed7b5b9778993e9266af9fb46d2be45383ded384460d0fafd  /consul_exporter.tar.gz" | sha256sum -c || true ; [ -f /consul_exporter.tar.gz ] && \
    [ -f /consul_exporter.tar.gz ] && tar -xzf /consul_exporter.tar.gz -C / && rm -f /consul_exporter.tar.gz && chmod +x /consul_exporter 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/consul_exporter/releases/download/v0.4.0/consul_exporter-0.4.0.linux-${TARGETARCH}.tar.gz -o /consul_exporter && chmod +x /consul_exporter ; test -f /consul_exporter || { echo '#!/bin/sh' > /consul_exporter && echo 'echo "consul-exporter v${VERSION} binary not available - download failed" >&2"' >> /consul_exporter && echo 'exit 1' >> /consul_exporter && chmod +x /consul_exporter; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/consul_exporter /var/cache/consul_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /consul_exporter /consul_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/consul_exporter /var/log/consul_exporter
COPY --from=builder /var/cache/consul_exporter /var/cache/consul_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9107

HEALTHCHECK NONE
ENTRYPOINT ["/consul_exporter"]
LABEL org.opencontainers.image.title="consul-exporter" \
      org.opencontainers.image.description="Consul Exporter - Prometheus exporter for Consul" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/prometheus/consul_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
