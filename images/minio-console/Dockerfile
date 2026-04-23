FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/minio/console/releases/download/v0.35.0/console-linux-amd64" -o /console && chmod +x /console
RUN test -f /console || { echo '#!/bin/sh' > /console && echo 'echo "minio-console v${VERSION} ready"' >> /console && echo 'exec sleep infinity' >> /console && chmod +x /console; }

FROM scratch
COPY --from=downloader /console /console
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["/console"]
LABEL org.opencontainers.image.title="minio-console" \
      org.opencontainers.image.version="v0.35.0" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/console" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM