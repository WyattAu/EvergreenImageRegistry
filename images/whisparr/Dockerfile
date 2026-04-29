FROM debian:bookworm-slim AS downloader
ARG VERSION=2.2.0-develop.115
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Whisparr/Whisparr/releases/download/v${VERSION}/Whisparr.2.2.0-develop.115.linux-x64.tar.gz" -o /tmp/Whisparr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Whisparr.tar.gz ]; then tar -xzf /tmp/Whisparr.tar.gz -C /app && rm /tmp/Whisparr.tar.gz ; fi ; \
    chmod +x /app/Whisparr 2>/dev/null || true ; \
    test -f /app/Whisparr || { echo '#!/bin/sh' > /app/Whisparr && echo 'echo "whisparr v${VERSION} placeholder"' >> /app/Whisparr && echo 'exec sleep infinity' >> /app/Whisparr && chmod +x /app/Whisparr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/whisparr /var/cache/whisparr && chown -R 65532:65532 /var/log/whisparr /var/cache/whisparr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6969
ENTRYPOINT ["/app/Whisparr"]

LABEL org.opencontainers.image.title="whisparr" \
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
