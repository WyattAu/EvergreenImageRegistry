ARG VERSION=latest
ARG TARGETARCH

FROM ghcr.io/nicbarker/minisearch:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="minisearch" org.opencontainers.image.version="best-effort" org.opencontainers.image.vendor="nicbarker" org.opencontainers.image.source="https://github.com/nicbarker/miniSearch" org.opencontainers.image.description="Lightweight full-text search engine" evergreen.image.tier="1" evergreen.image.category="search" evergreen.image.status="best-effort" evergreen.constraint.nonroot="true" evergreen.constraint.base="scratch" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/minisearch"]
