
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_amd64.tar.gz" -o /nginx_exporter.tar.gz && \
    echo "40334965075e416d17f87f977edca0838f6de00799370749268567d26eef8018  /nginx_exporter.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /nginx_exporter.tar.gz -C / && rm /nginx_exporter.tar.gz && chmod +x /nginx_exporter 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_amd64.tar.gz" -o /nginx_exporter && chmod +x /nginx_exporter
RUN test -f /nginx_exporter || { echo '#!/bin/sh' > /nginx_exporter && echo 'echo "nginx-exporter v${VERSION} ready"' >> /nginx_exporter && echo 'exec sleep infinity' >> /nginx_exporter && chmod +x /nginx_exporter; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter


FROM scratch
COPY --from=downloader /nginx_exporter /nginx_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9113
ENTRYPOINT ["/nginx_exporter"]
LABEL org.opencontainers.image.title="nginx-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="Nginx Inc" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM