ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.0.17.2953
ARG TARGETARCH
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.main.${VERSION}.linux-x64.tar.gz" -o /tmp/Sonarr.tar.gz ; \
    echo "d5142372067d727979421ca7b1d60601ceecd9758af3a7dafacc6ebba831777a  /tmp/Sonarr.tar.gz" | sha256sum -c ; \
    mkdir -p /app && \
    if [ -f /tmp/Sonarr.tar.gz ]; then tar -xzf /tmp/Sonarr.tar.gz -C /app && rm -f /tmp/Sonarr.tar.gz ; fi ; \
    chmod +x /app/Sonarr 2>/dev/null ; && { echo "Binary not available - download failed" >&2; exit 1; }

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65532:65532 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8989
EXPOSE 9101


LABEL org.opencontainers.image.description="sonarr-develop container image" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr" \
            org.opencontainers.image.version="4.0.17.2953"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8989"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="sonarr-develop" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
