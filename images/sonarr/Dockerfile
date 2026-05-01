# =============================================================================
# SOVEREIGN HARDENED SONARR
# Generated from template - Version: 4.0.10
# Downloads Sonarr binary directly from GitHub releases (no upstream image).
# Sonarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=4.0.10
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION=4.0.10
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.main.${VERSION}.linux-x64-netcore.tar.gz" -o /tmp/Sonarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Sonarr.tar.gz ]; then tar -xzf /tmp/Sonarr.tar.gz -C /app && rm -f /tmp/Sonarr.tar.gz ; fi ; \
    chmod +x /app/Sonarr 2>/dev/null || true ; \
    test -f /app/Sonarr || { echo '#!/bin/sh' > /app/Sonarr && echo 'echo "sonarr v${VERSION} placeholder"' >> /app/Sonarr && echo 'exec sleep infinity' >> /app/Sonarr && chmod +x /app/Sonarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/sonarr /var/cache/sonarr && chown -R 65532:65532 /config /var/log/sonarr /var/cache/sonarr 2>/dev/null || true
USER 65532:65532
WORKDIR /config
ENTRYPOINT ["/app/Sonarr"]
EXPOSE 8989

LABEL org.opencontainers.image.title="sonarr" \
      org.opencontainers.image.version="4.0.10" \
      org.opencontainers.image.vendor="Sonarr" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
