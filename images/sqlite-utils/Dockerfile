# =============================================================================
# SOVEREIGN HARDENED SQLITE-UTILS
# CLI tool for managing SQLite databases
# https://github.com/simonw/sqlite-utils
# =============================================================================

ARG VERSION=3.39
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
ARG BUILD_DATE
RUN apk add --no-cache ca-certificates tzdata python3 py3-pip && \
    pip install --no-cache-dir --break-system-packages "sqlite-utils==${VERSION}" && \
    addgroup -S -g 65532 sqlite 2>/dev/null || true && \
    adduser -u 65532 -G sqlite -D -h /data -s /bin/false sqlite 2>/dev/null || true && \
    mkdir -p /data && \
    chown -R 65532:65532 /data && \
    apk del py3-pip && \
    rm -rf /tmp/* /var/cache/apk/*

USER 65532:65532
WORKDIR /data
ENTRYPOINT ["sqlite-utils"]
LABEL org.opencontainers.image.title="sqlite-utils" \
      org.opencontainers.image.description="CLI tool for managing SQLite databases" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/simonw/sqlite-utils" \
      sovereign.image.tier="1" \
      sovereign.image.category="tooling" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="none"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
