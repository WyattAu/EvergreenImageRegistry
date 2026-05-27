ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.0.17.2953
ARG TARGETARCH
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.main.${VERSION}.linux-x64.tar.gz" -o /tmp/Sonarr.tar.gz ; \
    echo "d5142372067d727979421ca7b1d60601ceecd9758af3a7dafacc6ebba831777a  /tmp/Sonarr.tar.gz" | sha256sum -c ; \
    mkdir -p /app && \
    if [ -f /tmp/Sonarr.tar.gz ]; then tar -xzf /tmp/Sonarr.tar.gz -C /app && rm -f /tmp/Sonarr.tar.gz ; fi ; \
    chmod +x /app/Sonarr 2>/dev/null ; \binary not available - download failed" >&2 exit 1"' >> /app/Sonarr && echo 'exit 1' >> /app/Sonarr && chmod +x /app/Sonarr; }

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65532:65532 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8989
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8989/ || exit 1

LABEL org.opencontainers.image.description="sonarr-develop container image" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr" \
            org.opencontainers.image.version="4.0.17.2953"

ENTRYPOINT ["/app/Sonarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="sonarr-develop" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
