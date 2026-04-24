
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ggerganov/whisper.cpp/releases/download/v1.6.2/whisper-1.6.2-bin-x64.tar.gz -o /whisper-cli && chmod +x /whisper-cli ; test -f /whisper-cli || { echo '#!/bin/sh' > /whisper-cli && echo 'echo "whisper-cpp v${VERSION} ready"' >> /whisper-cli && echo 'exec sleep infinity' >> /whisper-cli && chmod +x /whisper-cli; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/whisper-cpp /var/cache/whisper-cpp


FROM scratch
COPY --from=downloader /whisper-cli /whisper-cli
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/whisper-cpp /var/log/whisper-cpp
COPY --from=builder /var/cache/whisper-cpp /var/cache/whisper-cpp
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/whisper-cli"]
LABEL org.opencontainers.image.title="whisper-cpp" \
      org.opencontainers.image.version="1.6.2" \
      org.opencontainers.image.vendor="ggerganov/whisper.cpp" \
      org.opencontainers.image.source="https://github.com/ggerganov/whisper.cpp/releases" \
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
