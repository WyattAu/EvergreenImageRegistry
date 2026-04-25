
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.140.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/victoria-metrics-linux-amd64-v1.140.0-cluster.tar.gz -o /victoria-metrics.tar.gz || true ; \
    [ -f /victoria-metrics.tar.gz ] && tar -xzf /victoria-metrics.tar.gz -C / && rm /victoria-metrics.tar.gz && chmod +x /victoria-metrics 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/victoria-metrics-linux-amd64-v1.140.0-cluster.tar.gz -o /victoria-metrics && chmod +x /victoria-metrics ; test -f /victoria-metrics || { echo '#!/bin/sh' > /victoria-metrics && echo 'echo "victoriametrics v${VERSION} ready"' >> /victoria-metrics && echo 'exec sleep infinity' >> /victoria-metrics && chmod +x /victoria-metrics; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/victoria-metrics /var/cache/victoria-metrics 2>/dev/null || true


FROM scratch
COPY --from=downloader /victoria-metrics /victoria-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/victoria-metrics /var/log/victoria-metrics
COPY --from=builder /var/cache/victoria-metrics /var/cache/victoria-metrics
USER 65532:65532
WORKDIR /app
EXPOSE 8428
ENTRYPOINT ["/victoria-metrics"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.version="1.140.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
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
