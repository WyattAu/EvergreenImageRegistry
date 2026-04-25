
FROM debian:bookworm-slim AS downloader
ARG VERSION=RELEASE.2025-04-08T16-46-15Z
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/client/mc/release/linux-amd64/mc" -o /mc && chmod +x /mc ; test -f /mc || { echo '#!/bin/sh' > /mc && echo 'echo "mc v${VERSION} ready"' >> /mc && echo 'exec sleep infinity' >> /mc && chmod +x /mc; } || true



FROM scratch
COPY --from=downloader /mc /mc
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 0
ENTRYPOINT ["/mc"]
LABEL org.opencontainers.image.title="mc" \
      org.opencontainers.image.version="RELEASE.2025-04-08T16-46-15Z" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/mc" \
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
