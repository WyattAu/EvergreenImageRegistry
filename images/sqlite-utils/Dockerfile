# =============================================================================
# EVERGREEN HARDENED SQLITE-UTILS
# CLI tool for managing SQLite databases
# https://github.com/simonw/sqlite-utils
# =============================================================================

ARG VERSION=3.39
ARG BUILD_DATE
ARG TARGETARCH

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["sqlite-utils"]
LABEL org.opencontainers.image.title="sqlite-utils" \
      org.opencontainers.image.description="CLI tool for managing SQLite databases" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/simonw/sqlite-utils" \
      evergreen.image.tier="1" \
      evergreen.image.category="tooling" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="none"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
