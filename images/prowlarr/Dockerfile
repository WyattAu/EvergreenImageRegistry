# =============================================================================
# EVERGREEN HARDENED PROWLARR
# Generated from template - Version: latest
# Downloads Prowlarr binary directly from GitHub releases (no upstream image).
# Prowlarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=1.27.0
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.27.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/Prowlarr/Prowlarr/releases/download/v${VERSION}/Prowlarr.master.${VERSION}.linux-x64-netcore.tar.gz" -o /tmp/Prowlarr.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/Prowlarr.tar.gz -C /app && rm -f /tmp/Prowlarr.tar.gz && \
    chmod +x /app/Prowlarr
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/prowlarr /var/cache/prowlarr && chown -R 65532:65532 /config /var/log/prowlarr /var/cache/prowlarr 2>/dev/null || true
USER 65532:65532
WORKDIR /config

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9696/ || exit 1
ENTRYPOINT ["/app/Prowlarr"]
EXPOSE 9696

LABEL org.opencontainers.image.title="prowlarr" \
      org.opencontainers.image.version="1.27.0" \
      org.opencontainers.image.vendor="Prowlarr" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr" \
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
