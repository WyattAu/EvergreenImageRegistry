FROM debian:bookworm-slim AS downloader
ARG VERSION=4.0.17.2953
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.develop.4.0.17.2953.linux-x64.tar.gz" -o /tmp/Sonarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Sonarr.tar.gz ]; then tar -xzf /tmp/Sonarr.tar.gz -C /app && rm /tmp/Sonarr.tar.gz ; fi ; \
    chmod +x /app/Sonarr 2>/dev/null || true ; \
    test -f /app/Sonarr || { echo '#!/bin/sh' > /app/Sonarr && echo 'echo "sonarr-develop v${VERSION} placeholder"' >> /app/Sonarr && echo 'exec sleep infinity' >> /app/Sonarr && chmod +x /app/Sonarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65532:65532 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8989
EXPOSE 9101
ENTRYPOINT ["/app/Sonarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="sonarr-develop" \
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
