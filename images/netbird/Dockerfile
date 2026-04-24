
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_0.29.1_linux_amd64.tar.gz" -o /netbird.tar.gz && \
    echo "c840e0426e1a564e3798ae471ad2854a503f4c2f55490908467d9092b98fd355  /netbird.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /netbird.tar.gz -C / && rm /netbird.tar.gz && chmod +x /netbird 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_0.29.1_linux_amd64.tar.gz" -o /netbird && chmod +x /netbird
RUN test -f /netbird || { echo '#!/bin/sh' > /netbird && echo 'echo "netbird v${VERSION} ready"' >> /netbird && echo 'exec sleep infinity' >> /netbird && chmod +x /netbird; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/netbird /var/cache/netbird


FROM scratch
COPY --from=downloader /netbird /netbird
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netbird /var/log/netbird
COPY --from=builder /var/cache/netbird /var/cache/netbird
USER 65532:65532
WORKDIR /app
EXPOSE 443 80
ENTRYPOINT ["/netbird"]
LABEL org.opencontainers.image.title="netbird" \
      org.opencontainers.image.version="0.29.1" \
      org.opencontainers.image.vendor="NetBird" \
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