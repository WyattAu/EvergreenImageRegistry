ARG VERSION=latest

FROM ghcr.io/nicbarker/minisearch:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/minisearch /var/cache/minisearch 2>/dev/null || true


FROM scratch
COPY --from=upstream /minisearch /minisearch
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/minisearch /var/log/minisearch
COPY --from=builder /var/cache/minisearch /var/cache/minisearch

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="minisearch" org.opencontainers.image.version="best-effort" org.opencontainers.image.vendor="nicbarker" org.opencontainers.image.source="https://github.com/nicbarker/miniSearch" org.opencontainers.image.description="Lightweight full-text search engine" sovereign.image.tier="1" sovereign.image.category="search" sovereign.image.status="best-effort" sovereign.constraint.nonroot="true" sovereign.constraint.base="scratch" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/minisearch"]
