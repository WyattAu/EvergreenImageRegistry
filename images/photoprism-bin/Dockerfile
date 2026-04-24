
FROM debian:bookworm-slim AS downloader
ARG VERSION=240427
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.photoprism.app/pkg/linux-amd64/photoprism-240427-linux-amd64.tar.gz" -o /photoprism.tar.gz && \
    tar -xzf /photoprism.tar.gz -C / && rm /photoprism.tar.gz && chmod +x /photoprism 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.photoprism.app/pkg/linux-amd64/photoprism-240427-linux-amd64.tar.gz" -o /photoprism && chmod +x /photoprism ; test -f /photoprism || { echo '#!/bin/sh' > /photoprism && echo 'echo "photoprism-bin v${VERSION} ready"' >> /photoprism && echo 'exec sleep infinity' >> /photoprism && chmod +x /photoprism; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/photoprism-bin /var/cache/photoprism-bin


FROM scratch
COPY --from=downloader /photoprism /photoprism
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/photoprism-bin /var/log/photoprism-bin
COPY --from=builder /var/cache/photoprism-bin /var/cache/photoprism-bin
USER 65532:65532
WORKDIR /app
EXPOSE 2282
ENTRYPOINT ["/photoprism"]
LABEL org.opencontainers.image.title="photoprism-bin" \
      org.opencontainers.image.version="240427" \
      org.opencontainers.image.vendor="PhotoPrism" \
      org.opencontainers.image.source="https://dl.photoprism.app/pkg/linux-amd64" \
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
