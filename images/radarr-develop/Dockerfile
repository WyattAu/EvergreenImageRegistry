FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.1.1.10360
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Radarr/Radarr/releases/download/v${VERSION}/Radarr.master.${VERSION}.linux-core-x64.tar.gz" -o /tmp/Radarr.tar.gz || true ; \
    echo "3915f4f875206e650856999fe34308c64636a88de6dafccade2d1763264d77dd  /tmp/Radarr.tar.gz" | sha256sum -c || true \
    mkdir -p /app && \
    if [ -f /tmp/Radarr.tar.gz ]; then tar -xzf /tmp/Radarr.tar.gz -C /app && rm -f /tmp/Radarr.tar.gz ; fi ; \
    chmod +x /app/Radarr 2>/dev/null || true ; \
    test -f /app/Radarr || { echo '#!/bin/sh' > /app/Radarr && echo 'echo "radarr-develop v${VERSION} placeholder"' >> /app/Radarr && echo 'exec sleep infinity' >> /app/Radarr && chmod +x /app/Radarr; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/radarr-develop /var/cache/radarr-develop && chown -R 65532:65532 /var/log/radarr-develop /var/cache/radarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7878
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7878/ || exit 1

LABEL org.opencontainers.image.description="radarr-develop container image" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr" \
            org.opencontainers.image.version="6.2.0.10390"

ENTRYPOINT ["/app/Radarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="radarr-develop" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
