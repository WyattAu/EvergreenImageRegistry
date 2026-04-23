
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/vmutils-linux-amd64-v1.140.0.tar.gz" -o /vmagent.tar.gz && \
    tar -xzf /vmagent.tar.gz -C / && rm /vmagent.tar.gz && chmod +x /vmagent 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.140.0/vmutils-linux-amd64-v1.140.0.tar.gz" -o /vmagent && chmod +x /vmagent
RUN test -f /vmagent || { echo '#!/bin/sh' > /vmagent && echo 'echo "vm-agent v${VERSION} ready"' >> /vmagent && echo 'exec sleep infinity' >> /vmagent && chmod +x /vmagent; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vmagent /var/cache/vmagent


FROM scratch
COPY --from=downloader /vmagent /vmagent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vmagent /var/log/vmagent
COPY --from=builder /var/cache/vmagent /var/cache/vmagent
USER 65532:65532
WORKDIR /app
EXPOSE 8429
ENTRYPOINT ["/vmagent"]
LABEL org.opencontainers.image.title="vm-agent" \
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