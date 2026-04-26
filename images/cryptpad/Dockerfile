ARG VERSION=2024.5.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/node /var/cache/node 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs ca-certificates curl || true
COPY --from=builder /app /app
RUN mkdir -p /app /var/log/node /var/cache/node ; \
    chown -R 65532:65532 /app /var/log/node /var/cache/nodeUSER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="cryptpad" \
      org.opencontainers.image.version="2024.5.1" \
      org.opencontainers.image.vendor="CryptPad" \
      org.opencontainers.image.source="https://github.com/cryptpad/cryptpad" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM