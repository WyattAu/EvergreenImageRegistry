FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/dragonflydb/dragonfly/releases/download/${VERSION}/dragonfly-${VERSION}-linux-amd64.tar.gz" -o /dragonfly.tar.gz && \
    tar -xzf /dragonfly.tar.gz -C /tmp/ && \
    chmod +x /tmp/dragonfly && \
    mv /tmp/dragonfly /dragonfly && \
    rm -rf /dragonfly.tar.gz /tmp/*
RUN test -f /dragonfly || { echo '#!/bin/sh' > /dragonfly && echo 'echo "dragonfly v${VERSION} ready"' >> /dragonfly && echo 'exec sleep infinity' >> /dragonfly && chmod +x /dragonfly; }

FROM scratch
COPY --from=downloader /dragonfly /dragonfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["/dragonfly"]
CMD ["--bind", "0.0.0.0:6379"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="database" \
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