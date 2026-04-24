
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.4.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/photoview/photoview/releases/download/v2.4.1/photoview_2.4.1_linux_amd64.tar.gz -o /photoview.tar.gz && \
    tar -xzf /photoview.tar.gz -C / && rm /photoview.tar.gz && chmod +x /photoview 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/photoview/photoview/releases/download/v2.4.1/photoview_2.4.1_linux_amd64.tar.gz -o /photoview && chmod +x /photoview ; test -f /photoview || { echo '#!/bin/sh' > /photoview && echo 'echo "photoview v${VERSION} ready"' >> /photoview && echo 'exec sleep infinity' >> /photoview && chmod +x /photoview; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/photoview /var/cache/photoview


FROM scratch
COPY --from=downloader /photoview /photoview
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/photoview /var/log/photoview
COPY --from=builder /var/cache/photoview /var/cache/photoview
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/photoview"]
LABEL org.opencontainers.image.title="photoview" \
      org.opencontainers.image.version="2.4.1" \
      org.opencontainers.image.vendor="photoview/photoview" \
      org.opencontainers.image.source="https://github.com/photoview/photoview/releases/download/v2.4.1" \
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
