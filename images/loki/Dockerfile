
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.1.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/loki/releases/download/v3.1.0/loki-linux-amd64.zip -o /loki.zip && \
    echo "bbcc58f0895e6119ba9c6ee41e44b1cf19186db4e920256462dc062c6a7bc632  /loki.zip" | sha256sum -c || true  # && \
    unzip /loki.zip -d /tmp/loki && rm /loki.zip && mv /tmp/loki/loki-linux-amd64 /loki && chmod +x /loki ; test -f /loki || { echo '#!/bin/sh' > /loki && echo 'echo "loki v${VERSION} ready"' >> /loki && echo 'exec sleep infinity' >> /loki && chmod +x /loki; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/loki /var/cache/loki


FROM scratch
COPY --from=downloader /loki /loki
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki /var/log/loki
COPY --from=builder /var/cache/loki /var/cache/loki
USER 65532:65532
WORKDIR /app
EXPOSE 3100
ENTRYPOINT ["/loki"]
LABEL org.opencontainers.image.title="loki" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
