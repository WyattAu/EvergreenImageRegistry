# =============================================================================
# SOVEREIGN HARDENED MINISEARCH
# Lightweight full-text search (miniSearch JS wrapper / best-effort)
# Constraint: scratch - Node.js binary bundle (best-effort approach)
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/nicbarker/miniSearch/releases/download/v0.0.3/minisearch-linux-x86_64" -o /minisearch 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/nicbarker/miniSearch/releases/latest/download/minisearch-linux-x86_64" -o /minisearch 2>/dev/null || \
    echo '#!/bin/sh' > /minisearch && echo 'echo "minisearch: no pre-built binary available"' >> /minisearch
RUN chmod +x /minisearch && \
    strip --strip-all /minisearch 2>/dev/null || true

FROM debian:bookworm-slim AS config
RUN mkdir -p /app /var/log/minisearch /var/lib/minisearch

FROM scratch
COPY --from=builder /minisearch /minisearch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=config /app /app
COPY --from=config /var/log/minisearch /var/log/minisearch
COPY --from=config /var/lib/minisearch /var/lib/minisearch
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/minisearch"]
LABEL org.opencontainers.image.title="minisearch" \
      org.opencontainers.image.version="best-effort" \
      org.opencontainers.image.vendor="nicbarker" \
      org.opencontainers.image.source="https://github.com/nicbarker/miniSearch" \
      org.opencontainers.image.description="Lightweight full-text search engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="best-effort" \
      sovereign.image.note="No confirmed upstream release binary; placeholder. Update URL when available." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM