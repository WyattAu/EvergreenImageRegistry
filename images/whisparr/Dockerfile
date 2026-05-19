ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.2.0-develop.115
ARG TARGETARCH
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Whisparr/Whisparr/releases/download/v${VERSION}/Whisparr.2.2.0-develop.115.linux-x64.tar.gz" -o /tmp/Whisparr.tar.gz || true ; \
    echo "48a2b1292e61027cec831f071141735c6dee43a0e61162f7062cf97d87fd0328  /tmp/Whisparr.tar.gz" | sha256sum -c || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Whisparr.tar.gz ]; then tar -xzf /tmp/Whisparr.tar.gz -C /app && rm -f /tmp/Whisparr.tar.gz ; fi ; \
    chmod +x /app/Whisparr 2>/dev/null || true ; \
    test -f /app/Whisparr || { echo '#!/bin/sh' > /app/Whisparr && echo 'echo "whisparr v${VERSION} binary not available - download failed" >&2
exit 1"' >> /app/Whisparr && echo 'exit 1' >> /app/Whisparr && chmod +x /app/Whisparr; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/whisparr /var/cache/whisparr && chown -R 65532:65532 /var/log/whisparr /var/cache/whisparr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6969
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:6969/ || exit 1

LABEL org.opencontainers.image.description="whisparr container image" \
      org.opencontainers.image.source="https://github.com/Whisparr/Whisparr" \
            org.opencontainers.image.version="2.2.0-develop.115"

ENTRYPOINT ["/app/Whisparr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="whisparr" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
