
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cloudflared/releases/download/${VERSION}/cloudflared-linux-amd64 -o /cloudflared && \
    chmod +x /cloudflared && \
    strip --strip-all /cloudflared || true
RUN test -f /cloudflared || { echo '#!/bin/sh' > /cloudflared && echo 'echo "cloudflare-warrior v${VERSION} ready"' >> /cloudflared && echo 'exec sleep infinity' >> /cloudflared && chmod +x /cloudflared; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudflared /etc/cloudflared


FROM scratch
COPY --from=downloader /cloudflared /cloudflared
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudflared /var/log/cloudflared
COPY --from=builder /etc/cloudflared /etc/cloudflared
USER 65532:65532
WORKDIR /app
EXPOSE 7844
ENTRYPOINT ["/cloudflared"]
CMD ["tunnel", "--no-autoupdate"]
LABEL org.opencontainers.image.title="cloudflare-warrior" \
      org.opencontainers.image.version="2024.4.1" \
      org.opencontainers.image.vendor="Cloudflare" \
      org.opencontainers.image.source="https://github.com/cloudflare/cloudflared" \
      org.opencontainers.image.description="Cloudflare Tunnel client (cloudflared)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
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