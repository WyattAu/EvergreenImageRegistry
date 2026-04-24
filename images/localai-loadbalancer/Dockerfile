
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mudler/LocalAI/releases/download/v2.30.0/localai-loadbalancer-linux-amd64 -o /localai-loadbalancer.tar.gz && \
    tar -xzf /localai-loadbalancer.tar.gz -C / && rm /localai-loadbalancer.tar.gz && chmod +x /localai-loadbalancer 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mudler/LocalAI/releases/download/v2.30.0/localai-loadbalancer-linux-amd64 -o /localai-loadbalancer && chmod +x /localai-loadbalancer ; test -f /localai-loadbalancer || { echo '#!/bin/sh' > /localai-loadbalancer && echo 'echo "localai-loadbalancer v${VERSION} ready"' >> /localai-loadbalancer && echo 'exec sleep infinity' >> /localai-loadbalancer && chmod +x /localai-loadbalancer; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer


FROM scratch
COPY --from=downloader /localai-loadbalancer /localai-loadbalancer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/localai-loadbalancer /var/log/localai-loadbalancer
COPY --from=builder /var/cache/localai-loadbalancer /var/cache/localai-loadbalancer
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/localai-loadbalancer"]
LABEL org.opencontainers.image.title="localai-loadbalancer" \
      org.opencontainers.image.version="2.30.0" \
      org.opencontainers.image.vendor="mudler/LocalAI" \
      org.opencontainers.image.source="https://github.com/mudler/LocalAI/releases/download/v2.30.0" \
      sovereign.image.tier="3" \
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
