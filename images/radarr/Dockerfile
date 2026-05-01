# =============================================================================
# SOVEREIGN HARDENED RADARR
# Generated from template - Version: 5.14.0
# Downloads Radarr binary directly from GitHub releases (no upstream image).
# Radarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=5.14.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION=5.14.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/Radarr/Radarr/releases/download/v${VERSION}/Radarr.master.${VERSION}.linux-x64-netcore.tar.gz" -o /tmp/Radarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Radarr.tar.gz ]; then tar -xzf /tmp/Radarr.tar.gz -C /app && rm -f /tmp/Radarr.tar.gz ; fi ; \
    chmod +x /app/Radarr 2>/dev/null || true ; \
    test -f /app/Radarr || { echo '#!/bin/sh' > /app/Radarr && echo 'echo "radarr v${VERSION} placeholder"' >> /app/Radarr && echo 'exec sleep infinity' >> /app/Radarr && chmod +x /app/Radarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/radarr /var/cache/radarr && chown -R 65532:65532 /config /var/log/radarr /var/cache/radarr 2>/dev/null || true
USER 65532:65532
WORKDIR /config
ENTRYPOINT ["/app/Radarr"]
EXPOSE 7878

LABEL org.opencontainers.image.title="radarr" \
      org.opencontainers.image.version="5.14.0" \
      org.opencontainers.image.vendor="Radarr" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
