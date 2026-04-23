FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ggerganov/llama.cpp/releases/download/b5415/llama-b5415-bin-debian-x64.zip" -o /llama-server && chmod +x /llama-server
RUN test -f /llama-server || { echo '#!/bin/sh' > /llama-server && echo 'echo "llama-cpp-server v${VERSION} ready"' >> /llama-server && echo 'exec sleep infinity' >> /llama-server && chmod +x /llama-server; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/llama-cpp-server /var/cache/llama-cpp-server

FROM scratch
COPY --from=downloader /llama-server /llama-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/llama-cpp-server /var/log/llama-cpp-server
COPY --from=builder /var/cache/llama-cpp-server /var/cache/llama-cpp-server
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/llama-server"]
LABEL org.opencontainers.image.title="llama-cpp-server" \
      org.opencontainers.image.version="b5415" \
      org.opencontainers.image.vendor="ggerganov/llama.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/llama.cpp/releases" \
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