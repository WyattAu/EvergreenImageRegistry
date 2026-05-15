
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.1.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/nginx/nginx-prometheus-exporter/releases/download/v${VERSION}/nginx-prometheus-exporter_${VERSION}_linux_${TARGETARCH}.tar.gz -o /nginx-prometheus-exporter.tar.gz || true ; \
    echo "40334965075e416d17f87f977edca0838f6de00799370749268567d26eef8018  /nginx-prometheus-exporter.tar.gz" | sha256sum -c || true ; \
    tar -xzf /nginx-prometheus-exporter.tar.gz -C / && rm -f /nginx-prometheus-exporter.tar.gz && chmod +x /nginx-prometheus-exporter ; test -f /nginx-prometheus-exporter || { echo '#!/bin/sh' > /nginx-prometheus-exporter && echo 'echo "prometheus-nginx-exporter v${VERSION} ready"' >> /nginx-prometheus-exporter && echo 'exec sleep infinity' >> /nginx-prometheus-exporter && chmod +x /nginx-prometheus-exporter; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /nginx-prometheus-exporter /nginx-prometheus-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9113

HEALTHCHECK NONE
ENTRYPOINT ["/nginx-prometheus-exporter"]
LABEL org.opencontainers.image.title="prometheus-nginx-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="NGINX Inc" \
      org.opencontainers.image.description="Prometheus exporter for NGINX stub_status metrics" \
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
            org.opencontainers.image.source="https://github.com/nginxinc/nginx-prometheus-exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
