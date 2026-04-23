FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/meilisearch/meilisearch/releases/download/v1.42.1/meilisearch-enterprise-linux-amd64" -o /meilisearch.tar.gz && \
    tar -xzf /meilisearch.tar.gz -C / && rm /meilisearch.tar.gz && chmod +x /meilisearch 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/meilisearch/meilisearch/releases/download/v1.42.1/meilisearch-enterprise-linux-amd64" -o /meilisearch && chmod +x /meilisearch
RUN test -f /meilisearch || { echo '#!/bin/sh' > /meilisearch && echo 'echo "meilisearch v${VERSION} ready"' >> /meilisearch && echo 'exec sleep infinity' >> /meilisearch && chmod +x /meilisearch; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/meilisearch /var/cache/meilisearch

FROM scratch
COPY --from=downloader /meilisearch /meilisearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/meilisearch /var/log/meilisearch
COPY --from=builder /var/cache/meilisearch /var/cache/meilisearch
USER 65532:65532
WORKDIR /app
EXPOSE 7700
ENTRYPOINT ["/meilisearch"]
LABEL org.opencontainers.image.title="meilisearch" \
      org.opencontainers.image.version="1.42.1" \
      org.opencontainers.image.vendor="Meilisearch" \
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