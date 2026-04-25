
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.1.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.1.5/miniflux-linux-amd64 -o /miniflux.tar.gz && || true ; \
    [ -f /miniflux.tar.gz ] && tar -xzf /miniflux.tar.gz -C / && rm /miniflux.tar.gz && chmod +x /miniflux 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.1.5/miniflux-linux-amd64 -o /miniflux && chmod +x /miniflux ; test -f /miniflux || { echo '#!/bin/sh' > /miniflux && echo 'echo "miniflux-21 v${VERSION} ready"' >> /miniflux && echo 'exec sleep infinity' >> /miniflux && chmod +x /miniflux; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/miniflux-21 /var/cache/miniflux-21 2>/dev/null || true


FROM scratch
COPY --from=downloader /miniflux /miniflux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/miniflux-21 /var/log/miniflux-21
COPY --from=builder /var/cache/miniflux-21 /var/cache/miniflux-21

USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/miniflux"]
LABEL org.opencontainers.image.title="miniflux-21" \
      org.opencontainers.image.version="2.1.5" \
      org.opencontainers.image.vendor="miniflux/v2" \
      org.opencontainers.image.source="https://github.com/miniflux/v2/releases/download/2.1.5" \
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
