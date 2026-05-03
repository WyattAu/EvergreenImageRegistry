# =============================================================================
# SOVEREIGN HARDENED JELLYFIN
# Generated from template - Version: 10.10.0
# Downloads Jellyfin server binary directly from official repo (no upstream image).
# Jellyfin is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=10.10.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION=10.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://repo.jellyfin.org/files/server/linux/latest-stable/amd64/jellyfin_${VERSION}-amd64.tar.gz" -o /tmp/jellyfin.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/jellyfin.tar.gz -C /app && rm -f /tmp/jellyfin.tar.gz && \
    chmod +x /app/jellyfin

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true
RUN adduser -u 65532 -D jellyfin 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /cache /media /var/log/jellyfin /var/cache/jellyfin && \
    chown -R 65532:65532 /config /cache /media /var/log/jellyfin /var/cache/jellyfin 2>/dev/null || true
USER 65532:65532
WORKDIR /config
ENTRYPOINT ["/app/jellyfin"]
EXPOSE 8096

LABEL org.opencontainers.image.title="jellyfin" \
      org.opencontainers.image.version="10.10.0" \
      org.opencontainers.image.vendor="Jellyfin" \
      org.opencontainers.image.source="https://github.com/jellyfin/jellyfin" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
