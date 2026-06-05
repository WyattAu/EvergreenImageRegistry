# =============================================================================
# EVERGREEN ALIAS - JELLYFIN-SERVER -> jellyfin
# Downloads Jellyfin server binary directly from official repo (no upstream image).
# Jellyfin is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=10.11.8
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=10.11.8
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://repo.jellyfin.org/files/server/linux/latest-stable/amd64/jellyfin_${VERSION}-amd64.tar.gz" -o /tmp/jellyfin.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/jellyfin.tar.gz -C /app && rm -f /tmp/jellyfin.tar.gz && \
    chmod +x /app/jellyfin
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null && \
    adduser -u 65532 -D jellyfin 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /cache /media /var/log/jellyfin-server /var/cache/jellyfin-server && \
    chown -R 65532:65532 /config /cache /media /var/log/jellyfin-server /var/cache/jellyfin-server 2>/dev/null || true
USER 65532:65532
WORKDIR /config

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8096"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
EXPOSE 8096

LABEL org.opencontainers.image.title="jellyfin-server" \
      org.opencontainers.image.description="jellyfin-server container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="media" \
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
