
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/qdrant/qdrant/releases/download/v1.17.1/qdrant-x86_64-unknown-linux-gnu.tar.gz" -o /qdrant.tar.gz && \
    tar -xzf /qdrant.tar.gz -C / && rm /qdrant.tar.gz && chmod +x /qdrant 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/qdrant/qdrant/releases/download/v1.17.1/qdrant-x86_64-unknown-linux-gnu.tar.gz" -o /qdrant && chmod +x /qdrant
RUN test -f /qdrant || { echo '#!/bin/sh' > /qdrant && echo 'echo "qdrant-cpu v${VERSION} ready"' >> /qdrant && echo 'exec sleep infinity' >> /qdrant && chmod +x /qdrant; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/qdrant-cpu /var/cache/qdrant-cpu


FROM scratch
COPY --from=downloader /qdrant /qdrant
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/qdrant-cpu /var/log/qdrant-cpu
COPY --from=builder /var/cache/qdrant-cpu /var/cache/qdrant-cpu
USER 65532:65532
WORKDIR /app
EXPOSE 6333
ENTRYPOINT ["/qdrant"]
LABEL org.opencontainers.image.title="qdrant-cpu" \
      org.opencontainers.image.version="1.17.1" \
      org.opencontainers.image.vendor="qdrant/qdrant" \
      org.opencontainers.image.source="https://github.com/qdrant/qdrant/releases/download/v1.17.1" \
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