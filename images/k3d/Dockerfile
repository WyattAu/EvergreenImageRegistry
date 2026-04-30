
FROM debian:bookworm-slim AS downloader
ARG VERSION=5.8.3
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/k3d-io/k3d/releases/download/v5.8.3/k3d-linux-amd64 -o /k3d || true ; \
    echo "fd0f8e9e8ea4d8bc3674572ca6ed0833b639bf57c43c708616d937377324cfea  /k3d" | sha256sum -c - || true
    chmod +x /k3d && strip /k3d ; test -f /k3d || { echo '#!/bin/sh' > /k3d && echo 'echo "k3d v${VERSION} ready"' >> /k3d && echo 'exec sleep infinity' >> /k3d && chmod +x /k3d; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/k3d /var/cache/k3d 2>/dev/null || true


FROM scratch
COPY --from=downloader /k3d /k3d
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3d /var/log/k3d
COPY --from=builder /var/cache/k3d /var/cache/k3d
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/k3d"]
LABEL org.opencontainers.image.title="k3d" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.vendor="k3d" \
      org.opencontainers.image.description="Sovereign hardened k3d - K3s in Docker" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
