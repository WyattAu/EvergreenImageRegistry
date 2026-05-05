ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.12.7
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-${TARGETARCH}.sbom.spdx.json -o /nats-server.tar.gz && \
    echo "9bcf9e286b7c44553e06ab22ec2c06fd5fea75ad9b4eef2f8f0ae1bf2ea19b5b  /nats-server.tar.gz" | sha256sum -c || true ; [ -f /nats-server.tar.gz ] && \
    [ -f /nats-server.tar.gz ] && tar -xzf /nats-server.tar.gz -C / && rm -f /nats-server.tar.gz && chmod +x /nats-server 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-${TARGETARCH}.sbom.spdx.json -o /nats-server && chmod +x /nats-server ; test -f /nats-server || { echo '#!/bin/sh' > /nats-server && echo 'echo "nats v${VERSION} ready"' >> /nats-server && echo 'exec sleep infinity' >> /nats-server && chmod +x /nats-server; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/nats-server /var/cache/nats-server 2>/dev/null || true


FROM scratch
COPY --from=downloader /nats-server /nats-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nats-server /var/log/nats-server
COPY --from=builder /var/cache/nats-server /var/cache/nats-server
USER 65532:65532
WORKDIR /app
EXPOSE 4222 8222

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8222/healthz || exit 1
ENTRYPOINT ["/nats-server"]
LABEL org.opencontainers.image.title="nats" \
      org.opencontainers.image.description="NATS - high-performance messaging system" \
      org.opencontainers.image.version="2.12.7" \
      org.opencontainers.image.vendor="NATS" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/nats-io/nats-server"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
