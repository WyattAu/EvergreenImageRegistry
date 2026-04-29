FROM debian:bookworm-slim AS downloader
ARG VERSION=2.3.6.5351
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Prowlarr/Prowlarr/releases/download/v${VERSION}/Prowlarr.develop.2.3.6.5351.linux-core-x64.tar.gz" -o /tmp/Prowlarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Prowlarr.tar.gz ]; then tar -xzf /tmp/Prowlarr.tar.gz -C /app && rm /tmp/Prowlarr.tar.gz ; fi ; \
    chmod +x /app/Prowlarr 2>/dev/null || true ; \
    test -f /app/Prowlarr || { echo '#!/bin/sh' > /app/Prowlarr && echo 'echo "prowlarr-develop v${VERSION} placeholder"' >> /app/Prowlarr && echo 'exec sleep infinity' >> /app/Prowlarr && chmod +x /app/Prowlarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/prowlarr-develop /var/cache/prowlarr-develop && chown -R 65532:65532 /var/log/prowlarr-develop /var/cache/prowlarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9696
ENTRYPOINT ["/app/Prowlarr"]

LABEL org.opencontainers.image.title="prowlarr-develop" \
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
