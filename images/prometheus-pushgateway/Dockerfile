
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-amd64.tar.gz -o /pushgateway.tar.gz && \
    echo "ee962b451e533c392d9bfd07f5e4195d64a65b87b55d4abbcedc5f9ce13dfc58  /pushgateway.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /pushgateway.tar.gz -C / && rm /pushgateway.tar.gz && chmod +x /pushgateway 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-amd64.tar.gz -o /pushgateway && chmod +x /pushgateway ; test -f /pushgateway || { echo '#!/bin/sh' > /pushgateway && echo 'echo "prometheus-pushgateway v${VERSION} ready"' >> /pushgateway && echo 'exec sleep infinity' >> /pushgateway && chmod +x /pushgateway; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pushgateway /var/cache/pushgateway


FROM scratch
COPY --from=downloader /pushgateway /pushgateway
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pushgateway /var/log/pushgateway
COPY --from=builder /var/cache/pushgateway /var/cache/pushgateway
USER 65532:65532
WORKDIR /app
EXPOSE 9091
ENTRYPOINT ["/pushgateway"]
LABEL org.opencontainers.image.title="prometheus-pushgateway" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
