ARG VERSION=latest

FROM ghcr.io/quickwit-oss/tantivy:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tantivy /var/cache/tantivy 2>/dev/null || true


FROM scratch
COPY --from=upstream /tantivy /tantivy
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tantivy /var/log/tantivy
COPY --from=builder /var/cache/tantivy /var/cache/tantivy

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="tantivy" org.opencontainers.image.version="0.22.0" org.opencontainers.image.vendor="quickwit-oss" org.opencontainers.image.source="https://github.com/quickwit-oss/tantivy-cli" org.opencontainers.image.description="Full-text search engine CLI" sovereign.image.tier="1" sovereign.image.category="search" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="scratch" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="2000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/tantivy"]
