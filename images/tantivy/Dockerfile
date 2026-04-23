# =============================================================================
# SOVEREIGN HARDENED TANTIVY
# Full-text search engine (Rust CLI)
# Constraint: scratch - static Rust binary (musl)
# =============================================================================

ARG VERSION=0.22.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/quickwit-oss/tantivy-cli/releases/download/v${VERSION}/tantivy-cli-v${VERSION}-x86_64-unknown-linux-musl.tar.gz" -o /tantivy.tar.gz && \
    tar -xzf /tantivy.tar.gz -C / && rm /tantivy.tar.gz && \
    find / -maxdepth 2 -name "tantivy" -type f -exec chmod +x {} \;

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tantivy /var/lib/tantivy

FROM scratch
COPY --from=downloader /tantivy /tantivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tantivy /var/log/tantivy
COPY --from=builder /var/lib/tantivy /var/lib/tantivy
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/tantivy"]
LABEL org.opencontainers.image.title="tantivy" \
      org.opencontainers.image.version="0.22.0" \
      org.opencontainers.image.vendor="quickwit-oss" \
      org.opencontainers.image.source="https://github.com/quickwit-oss/tantivy-cli" \
      org.opencontainers.image.description="Full-text search engine CLI" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="2000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM