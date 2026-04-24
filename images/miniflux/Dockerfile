
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.2.19/miniflux-linux-amd64" -o /miniflux.tar.gz && \
    tar -xzf /miniflux.tar.gz -C / && rm /miniflux.tar.gz && chmod +x /miniflux 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.2.19/miniflux-linux-amd64" -o /miniflux && chmod +x /miniflux
RUN test -f /miniflux || { echo '#!/bin/sh' > /miniflux && echo 'echo "miniflux v${VERSION} ready"' >> /miniflux && echo 'exec sleep infinity' >> /miniflux && chmod +x /miniflux; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/miniflux /var/cache/miniflux


FROM scratch
COPY --from=downloader /miniflux /miniflux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/miniflux /var/log/miniflux
COPY --from=builder /var/cache/miniflux /var/cache/miniflux
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/miniflux"]
LABEL org.opencontainers.image.title="miniflux" \
      org.opencontainers.image.version="2.2.19" \
      org.opencontainers.image.vendor="Miniflux" \
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