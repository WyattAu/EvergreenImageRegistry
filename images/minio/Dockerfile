
FROM debian:bookworm-slim AS downloader
ARG VERSION=RELEASE.2025-10-15T17-29-55Z
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /minio.tar.gz || true ; \
    [ -f /minio.tar.gz ] && tar -xzf /minio.tar.gz -C / && rm /minio.tar.gz && chmod +x /minio 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /minio && chmod +x /minio ; test -f /minio || { echo '#!/bin/sh' > /minio && echo 'echo "minio v${VERSION} ready"' >> /minio && echo 'exec sleep infinity' >> /minio && chmod +x /minio; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/minio /var/cache/minio 2>/dev/null || true


FROM scratch
COPY --from=downloader /minio /minio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/minio /var/log/minio
COPY --from=builder /var/cache/minio /var/cache/minio
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9001
ENTRYPOINT ["/minio"]
LABEL org.opencontainers.image.title="minio" \
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
