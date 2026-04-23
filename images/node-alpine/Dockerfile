ARG VERSION=v22.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz" -o /node.tar.xz && \
    mkdir -p /opt/node && tar -xf /node.tar.xz -C /opt/node --strip-components=1 && rm /node.tar.xz && \
    strip /opt/node/bin/node 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/node-alpine /var/cache/node-alpine

FROM scratch
COPY --from=downloader /opt/node /opt/node
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/node-alpine /var/log/node-alpine
COPY --from=builder /var/cache/node-alpine /var/cache/node-alpine
ENV PATH="/opt/node/bin:${PATH}" \
    NODE_ENV=production
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="node-alpine" \
      org.opencontainers.image.version="22.12.0" \
      org.opencontainers.image.vendor="Node.js" \
      org.opencontainers.image.description="Sovereign hardened node-alpine - Node.js runtime (no Alpine, scratch)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM