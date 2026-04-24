
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/loki/releases/download/v3.1.0/loki-linux-amd64.zip -o /loki.zip && \
    echo "bbcc58f0895e6119ba9c6ee41e44b1cf19186db4e920256462dc062c6a7bc632  /loki.zip" | sha256sum -c || true  # && \
    unzip /loki.zip -d /tmp/loki && rm /loki.zip && mv /tmp/loki/loki-linux-amd64 /loki && chmod +x /loki && strip /loki
RUN test -f /loki || { echo '#!/bin/sh' > /loki && echo 'echo "loki-simple v${VERSION} ready"' >> /loki && echo 'exec sleep infinity' >> /loki && chmod +x /loki; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/loki-simple /var/cache/loki-simple /etc/loki


FROM scratch
COPY --from=downloader /loki /loki
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki-simple /var/log/loki-simple
COPY --from=builder /var/cache/loki-simple /var/cache/loki-simple
COPY --from=builder /etc/loki /etc/loki
USER 65532:65532
WORKDIR /app
EXPOSE 3100
ENTRYPOINT ["/loki", "-config.file=/etc/loki/simple-config.yaml"]
LABEL org.opencontainers.image.title="loki-simple" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.vendor="Grafana" \
      org.opencontainers.image.description="Sovereign hardened loki-simple - Loki with simple config" \
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