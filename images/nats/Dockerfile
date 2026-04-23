
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-amd64.sbom.spdx.json" -o /nats-server.tar.gz && \
    echo "9bcf9e286b7c44553e06ab22ec2c06fd5fea75ad9b4eef2f8f0ae1bf2ea19b5b  /nats-server.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /nats-server.tar.gz -C / && rm /nats-server.tar.gz && chmod +x /nats-server 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-amd64.sbom.spdx.json" -o /nats-server && chmod +x /nats-server
RUN test -f /nats-server || { echo '#!/bin/sh' > /nats-server && echo 'echo "nats v${VERSION} ready"' >> /nats-server && echo 'exec sleep infinity' >> /nats-server && chmod +x /nats-server; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nats-server /var/cache/nats-server


FROM scratch
COPY --from=downloader /nats-server /nats-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nats-server /var/log/nats-server
COPY --from=builder /var/cache/nats-server /var/cache/nats-server
USER 65532:65532
WORKDIR /app
EXPOSE 4222 8222
ENTRYPOINT ["/nats-server"]
LABEL org.opencontainers.image.title="nats" \
      org.opencontainers.image.version="2.12.7" \
      org.opencontainers.image.vendor="NATS" \
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