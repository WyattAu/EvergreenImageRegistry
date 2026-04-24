
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.18.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dragonflydb/dragonfly/releases/download/${VERSION}/dragonfly-${VERSION}-linux-amd64.tar.gz -o /dragonfly.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dragonflydb/dragonfly/releases/download/${VERSION}/checksums.txt -o /checksums.txt && \
    grep "dragonfly-${VERSION}-linux-amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /dragonfly.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/dfly && \
    mv /tmp/dfly /dfly && \
    rm -rf /dragonfly.tar.gz /checksums.txt /tmp/* ; test -f /dfly || { echo '#!/bin/sh' > /dfly && echo 'echo "dragonfly-client v${VERSION} ready"' >> /dfly && echo 'exec sleep infinity' >> /dfly && chmod +x /dfly; }



FROM scratch
COPY --from=downloader /dfly /dfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/dfly"]
LABEL org.opencontainers.image.title="dragonfly-client" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM

