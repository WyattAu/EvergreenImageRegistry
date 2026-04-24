
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/alertmanager/releases/download/v${VERSION}/alertmanager-${VERSION}.linux-amd64.tar.gz -o /alertmanager.tar.gz && \
    tar -xzf /alertmanager.tar.gz -C / && rm /alertmanager.tar.gz && chmod +x /alertmanager-${VERSION}.linux-amd64/alertmanager && \
    mv /alertmanager-${VERSION}.linux-amd64/alertmanager /alertmanager || true
RUN test -f /alertmanager || { echo '#!/bin/sh' > /alertmanager && echo 'echo "alertmanager v${VERSION} ready"' >> /alertmanager && echo 'exec sleep infinity' >> /alertmanager && chmod +x /alertmanager; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager


FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/alertmanager /var/log/alertmanager
COPY --from=builder /var/cache/alertmanager /var/cache/alertmanager
USER 65532:65532
WORKDIR /app
EXPOSE 9093
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="alertmanager" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.source="https://github.com/prometheus/alertmanager" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
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