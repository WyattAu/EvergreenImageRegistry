# =============================================================================
# EVERGREEN HARDENED LIDARR
# Generated from template - Version: latest
# Downloads Lidarr binary directly from GitHub releases (no upstream image).
# Lidarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=3.1.0.4875
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.1.0.4875
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Lidarr/Lidarr/releases/download/v${VERSION}/Lidarr.master.${VERSION}.linux-core-x64.tar.gz" -o /tmp/Lidarr.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/Lidarr.tar.gz -C /app && rm -f /tmp/Lidarr.tar.gz && \
    chmod +x /app/Lidarr
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/lidarr /var/cache/lidarr && chown -R 65532:65532 /config /var/log/lidarr /var/cache/lidarr 2>/dev/null || true
USER 65532:65532
WORKDIR /config

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8686/ || exit 1
ENTRYPOINT ["/app/Lidarr"]
EXPOSE 8686

LABEL org.opencontainers.image.title="lidarr" \
      org.opencontainers.image.description="Lidarr - music collection manager for Usenet and BitTorrent" \
      org.opencontainers.image.version="2.4.3" \
      org.opencontainers.image.vendor="Lidarr" \
      org.opencontainers.image.source="https://github.com/Lidarr/Lidarr" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.official="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
