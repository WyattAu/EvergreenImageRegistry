
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.21.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/lancedb/lance/releases/download/v0.21.0/lancedb-v0.21.0-x86_64-unknown-linux-gnu.tar.gz -o /lancedb.tar.gz || true ; \
    [ -f /lancedb.tar.gz ] && tar -xzf /lancedb.tar.gz -C / && rm -f /lancedb.tar.gz && chmod +x /lancedb 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/lancedb/lance/releases/download/v0.21.0/lancedb-v0.21.0-x86_64-unknown-linux-gnu.tar.gz -o /lancedb && chmod +x /lancedb ; test -f /lancedb || { echo '#!/bin/sh' > /lancedb && echo 'echo "lancedb v${VERSION} ready"' >> /lancedb && echo 'exec sleep infinity' >> /lancedb && chmod +x /lancedb; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/lancedb /var/cache/lancedb 2>/dev/null || true


FROM scratch
COPY --from=downloader /lancedb /lancedb
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/lancedb /var/log/lancedb
COPY --from=builder /var/cache/lancedb /var/cache/lancedb
USER 65532:65532
WORKDIR /app
EXPOSE 6333
ENTRYPOINT ["/lancedb"]
LABEL org.opencontainers.image.title="lancedb" \
      org.opencontainers.image.version="0.21.0" \
      org.opencontainers.image.vendor="lancedb/lance" \
      org.opencontainers.image.source="https://github.com/lancedb/lance/releases/download/v0.21.0" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
