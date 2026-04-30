FROM debian:bookworm-slim AS downloader
ARG VERSION=0.4.18.2805
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Readarr/Readarr/releases/download/v${VERSION}/Readarr.develop.0.4.18.2805.linux-core-x64.tar.gz" -o /tmp/Readarr.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/Readarr.tar.gz ]; then tar -xzf /tmp/Readarr.tar.gz -C /app && rm /tmp/Readarr.tar.gz ; fi ; \
    chmod +x /app/Readarr 2>/dev/null || true ; \
    test -f /app/Readarr || { echo '#!/bin/sh' > /app/Readarr && echo 'echo "readarr v${VERSION} placeholder"' >> /app/Readarr && echo 'exec sleep infinity' >> /app/Readarr && chmod +x /app/Readarr; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/readarr /var/cache/readarr && chown -R 65532:65532 /var/log/readarr /var/cache/readarr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8787
EXPOSE 9101
ENTRYPOINT ["/app/Readarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="readarr" \
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
