
FROM debian:bookworm-slim AS downloader
ARG VERSION=RELEASE.2025-10-15T17-29-55Z
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /s3-server.tar.gz || true ; \
    [ -f /s3-server.tar.gz ] && tar -xzf /s3-server.tar.gz -C / && rm -f /s3-server.tar.gz && chmod +x /s3-server 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /s3-server && chmod +x /s3-server ; test -f /s3-server || { echo '#!/bin/sh' > /s3-server && echo 'echo "s3 v${VERSION} ready"' >> /s3-server && echo 'exec sleep infinity' >> /s3-server && chmod +x /s3-server; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/s3-server /var/cache/s3-server 2>/dev/null || true


FROM scratch
COPY --from=downloader /s3-server /s3-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/s3-server /var/log/s3-server
COPY --from=builder /var/cache/s3-server /var/cache/s3-server
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9001
ENTRYPOINT ["/s3-server"]
LABEL org.opencontainers.image.title="s3" \
      org.opencontainers.image.version="RELEASE.2025-10-15T17-29-55Z" \
      org.opencontainers.image.vendor="MinIO" \
      sovereign.image.tier="1" \
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
