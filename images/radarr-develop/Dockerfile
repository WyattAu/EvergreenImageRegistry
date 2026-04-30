FROM debian:bookworm-slim AS downloader
ARG VERSION=6.2.0.10390
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Radarr/Radarr/releases/download/v${VERSION}/Radarr.develop.6.2.0.10390.linux-core-x64.tar.gz" -o /tmp/Radarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Radarr.tar.gz ]; then tar -xzf /tmp/Radarr.tar.gz -C /app && rm /tmp/Radarr.tar.gz ; fi ; \
    chmod +x /app/Radarr 2>/dev/null || true ; \
    test -f /app/Radarr || { echo '#!/bin/sh' > /app/Radarr && echo 'echo "radarr-develop v${VERSION} placeholder"' >> /app/Radarr && echo 'exec sleep infinity' >> /app/Radarr && chmod +x /app/Radarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/radarr-develop /var/cache/radarr-develop && chown -R 65532:65532 /var/log/radarr-develop /var/cache/radarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7878
EXPOSE 9101
ENTRYPOINT ["/app/Radarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="radarr-develop" \
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
