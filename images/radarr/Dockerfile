# =============================================================================
# EVERGREEN HARDENED RADARR
# Generated from template - Version: 5.14.0
# Downloads Radarr binary directly from GitHub releases (no upstream image).
# Radarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=5.14.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.14.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/Radarr/Radarr/releases/download/v${VERSION}/Radarr.master.${VERSION}.linux-x64-netcore.tar.gz" -o /tmp/Radarr.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/Radarr.tar.gz -C /app && rm -f /tmp/Radarr.tar.gz && \
    chmod +x /app/Radarr

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/radarr /var/cache/radarr && chown -R 65532:65532 /config /var/log/radarr /var/cache/radarr 2>/dev/null || true
USER 65532:65532
WORKDIR /config

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7878/ || exit 1
ENTRYPOINT ["/app/Radarr"]
EXPOSE 7878

LABEL org.opencontainers.image.title="radarr" \
      org.opencontainers.image.version="5.14.0" \
      org.opencontainers.image.vendor="Radarr" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.official="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
