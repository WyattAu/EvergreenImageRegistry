# =============================================================================
# EVERGREEN HARDENED JELLYFIN
# Generated from template - Version: 10.11.8
# Downloads Jellyfin server binary directly from official repo (no upstream image).
# Jellyfin is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=10.11.8
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=10.11.8
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://repo.jellyfin.org/files/server/linux/latest-stable/amd64/jellyfin_${VERSION}-amd64.tar.gz" -o /tmp/jellyfin.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/jellyfin.tar.gz -C /app && rm -f /tmp/jellyfin.tar.gz && \
    chmod +x /app/jellyfin
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true && \
    adduser -u 65532 -D jellyfin 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /cache /media /var/log/jellyfin /var/cache/jellyfin && \
    chown -R 65532:65532 /config /cache /media /var/log/jellyfin /var/cache/jellyfin 2>/dev/null || true
USER 65532:65532
WORKDIR /config

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8096/ || exit 1
ENTRYPOINT ["/app/jellyfin"]
EXPOSE 8096

LABEL org.opencontainers.image.title="jellyfin" \
      org.opencontainers.image.description="Jellyfin - free software media system" \
      org.opencontainers.image.version="10.11.8" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin" \
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
