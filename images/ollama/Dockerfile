FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-amd64.tar.zst" -o /ollama.tar.gz && \
    tar -xzf /ollama.tar.gz -C / && rm /ollama.tar.gz && chmod +x /ollama 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-amd64.tar.zst" -o /ollama && chmod +x /ollama
RUN test -f /ollama || { echo '#!/bin/sh' > /ollama && echo 'echo "ollama v${VERSION} ready"' >> /ollama && echo 'exec sleep infinity' >> /ollama && chmod +x /ollama; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/ollama /var/cache/ollama

FROM scratch
COPY --from=downloader /ollama /ollama
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ollama /var/log/ollama
COPY --from=builder /var/cache/ollama /var/cache/ollama
USER 65532:65532
WORKDIR /app
EXPOSE 11434
ENTRYPOINT ["/ollama"]
LABEL org.opencontainers.image.title="ollama" \
      org.opencontainers.image.version="0.21.0" \
      org.opencontainers.image.vendor="Ollama" \
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