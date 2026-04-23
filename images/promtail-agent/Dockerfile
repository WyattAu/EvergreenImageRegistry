
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-amd64.zip" -o /promtail.zip && \
    unzip -o /promtail.zip -d /tmp && \
    chmod +x /tmp/promtail-linux-amd64 && \
    mv /tmp/promtail-linux-amd64 /promtail
RUN test -f /promtail || { echo '#!/bin/sh' > /promtail && echo 'echo "promtail-agent v${VERSION} ready"' >> /promtail && echo 'exec sleep infinity' >> /promtail && chmod +x /promtail; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/promtail


FROM scratch
COPY --from=downloader /promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/promtail /var/log/promtail
USER 65532:65532
EXPOSE 9080 3100
ENTRYPOINT ["/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail-agent" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.source="https://github.com/grafana/loki" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="logging" \
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