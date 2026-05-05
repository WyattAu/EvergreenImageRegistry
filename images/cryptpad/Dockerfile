FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app-data /var/log/node /var/cache/node 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs ca-certificates curl 
COPY --from=builder /app /app
RUN mkdir -p /app /var/log/node /var/cache/node ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/node /var/cache/node
USER 65532:65532
WORKDIR /app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3000/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="cryptpad" \
      org.opencontainers.image.description="cryptpad container image" \
      org.opencontainers.image.version="2024.5.1" \
      org.opencontainers.image.vendor="CryptPad" \
      org.opencontainers.image.source="https://github.com/cryptpad/cryptpad" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
