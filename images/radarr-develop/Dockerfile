ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.2.0.10390
ARG TARGETARCH
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Radarr/Radarr/releases/download/v${VERSION}/Radarr.master.${VERSION}.linux-core-x64.tar.gz" -o /tmp/Radarr.tar.gz ; \
    echo "3915f4f875206e650856999fe34308c64636a88de6dafccade2d1763264d77dd  /tmp/Radarr.tar.gz" | sha256sum -c ; \
    mkdir -p /app && \
    if [ -f /tmp/Radarr.tar.gz ]; then tar -xzf /tmp/Radarr.tar.gz -C /app && rm -f /tmp/Radarr.tar.gz ; fi ; \
    chmod +x /app/Radarr 2>/dev/null ; && { echo "Binary not available - download failed" >&2; exit 1; }

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/radarr-develop /var/cache/radarr-develop && chown -R 65532:65532 /var/log/radarr-develop /var/cache/radarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7878
EXPOSE 9101


LABEL org.opencontainers.image.description="radarr-develop container image" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr" \
            org.opencontainers.image.version="6.2.0.10390"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7878"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="radarr-develop" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
