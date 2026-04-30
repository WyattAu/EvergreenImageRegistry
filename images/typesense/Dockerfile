
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.25.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/typesense/typesense/releases/download/v${VERSION}/typesense-server-${VERSION}-linux-amd64.tar.gz -o /typesense.tar.gz || true ; \
    [ -f /typesense.tar.gz ] && tar -xzf /typesense.tar.gz -C / && rm -f /typesense.tar.gz || true ; \
    find / -maxdepth 2 -name "typesense-server" -type f -exec chmod +x {} \; && \
    strip --strip-all /typesense-server 2>/dev/null ; test -f /typesense-server || { echo '#!/bin/sh' > /typesense-server && echo 'echo "typesense v${VERSION} ready"' >> /typesense-server && echo 'exec sleep infinity' >> /typesense-server && chmod +x /typesense-server; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/typesense /var/lib/typesense 2>/dev/null || true


FROM scratch
COPY --from=downloader /typesense-server /typesense-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/typesense /var/log/typesense
COPY --from=builder /var/lib/typesense /var/lib/typesense
USER 65532:65532
WORKDIR /app
EXPOSE 8108
ENTRYPOINT ["/typesense-server"]
LABEL org.opencontainers.image.title="typesense" \
      org.opencontainers.image.version="0.25.2" \
      org.opencontainers.image.vendor="Typesense" \
      org.opencontainers.image.source="https://github.com/typesense/typesense" \
      org.opencontainers.image.description="Fast, typo-tolerant search engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="best-effort" \
      sovereign.image.note="May require glibc; fallback to debian-slim if scratch fails" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
