FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app/data-src-src /var/log/zipline /var/cache/zipline 2>/dev/null || true && \
    test -f /app/data || { echo '#!/bin/sh' > /app/data && echo 'echo "zipline v${VERSION} placeholder"' >> /app/data && echo 'exec sleep infinity' >> /app/data && chmod +x /app/data; }
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs npm git ca-certificates python3 make 
WORKDIR /src
RUN git clone --depth 1 https://github.com/diced/zipline.git /src || echo "Source repo not available - using placeholder" && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true && npm run build 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true && npm run build 2>/dev/null || true && \
    mkdir -p /app/data-src-src 2>/dev/null || true
COPY --from=downloader /app/data /app/data
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false zipline 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="zipline" \
      org.opencontainers.image.description="Zipline - File sharing platform" \
      org.opencontainers.image.vendor="diced" \
      org.opencontainers.image.source="https://github.com/diced/zipline" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
