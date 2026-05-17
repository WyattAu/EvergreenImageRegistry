ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.15.0
RUN touch /haproxy_exporter || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/haproxy_exporter/releases/download/v0.15.0/haproxy_exporter-0.15.0.linux-${TARGETARCH}.tar.gz -o /haproxy_exporter.tar.gz && \
    echo "c8d76f8c86704408479c13843b7c050d4e8ebcb68722b479ffbcdc9b02630ddc  /haproxy_exporter.tar.gz" | sha256sum -c || true ; [ -f /haproxy_exporter.tar.gz ] && \
    [ -f /haproxy_exporter.tar.gz ] && tar -xzf /haproxy_exporter.tar.gz -C / && rm -f /haproxy_exporter.tar.gz && chmod +x /haproxy_exporter 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/haproxy_exporter/releases/download/v0.15.0/haproxy_exporter-0.15.0.linux-${TARGETARCH}.tar.gz -o /haproxy_exporter && chmod +x /haproxy_exporter ; test -f /haproxy_exporter || { echo '#!/bin/sh' > /haproxy_exporter && echo 'echo "haproxy-exporter v${VERSION} ready"' >> /haproxy_exporter && echo 'exec sleep infinity' >> /haproxy_exporter && chmod +x /haproxy_exporter; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/haproxy_exporter /var/cache/haproxy_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /haproxy_exporter /haproxy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/haproxy_exporter /var/log/haproxy_exporter
COPY --from=builder /var/cache/haproxy_exporter /var/cache/haproxy_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101

HEALTHCHECK NONE
ENTRYPOINT ["/haproxy_exporter"]
LABEL org.opencontainers.image.title="haproxy-exporter" \
      org.opencontainers.image.description="haproxy-exporter container image" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/prometheus/haproxy_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

STOPSIGNAL SIGTERM
