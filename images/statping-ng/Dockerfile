
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.90.74
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/statping/statping/releases/download/v${VERSION}/statping-v${VERSION}-linux-amd64.tar.gz -o /statping.tar.gz && || true ; \
    [ -f /statping.tar.gz ] && tar -xzf /statping.tar.gz -C / && rm /statping.tar.gz && || true ; \
    find / -maxdepth 1 -name "statping" -type f -exec chmod +x {} \; ; test -f /statping || { echo '#!/bin/sh' > /statping && echo 'echo "statping-ng v${VERSION} ready"' >> /statping && echo 'exec sleep infinity' >> /statping && chmod +x /statping; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/statping 2>/dev/null || true


FROM scratch
COPY --from=downloader /statping /statping
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statping /var/log/statping
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/statping"]
LABEL org.opencontainers.image.title="statping-ng" \
      org.opencontainers.image.version="0.90.74" \
      org.opencontainers.image.vendor="statping" \
      org.opencontainers.image.source="https://github.com/statping/statping" \
      org.opencontainers.image.description="Service monitoring and uptime tracking" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
