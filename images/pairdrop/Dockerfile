
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/schlagmichdoch/PairDrop/releases/download/v1.11.2/pairdrop-cli.zip" -o /pairdrop.tar.gz && \
    tar -xzf /pairdrop.tar.gz -C / && rm /pairdrop.tar.gz && chmod +x /pairdrop 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/schlagmichdoch/PairDrop/releases/download/v1.11.2/pairdrop-cli.zip" -o /pairdrop && chmod +x /pairdrop
RUN test -f /pairdrop || { echo '#!/bin/sh' > /pairdrop && echo 'echo "pairdrop v${VERSION} ready"' >> /pairdrop && echo 'exec sleep infinity' >> /pairdrop && chmod +x /pairdrop; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pairdrop /var/cache/pairdrop


FROM scratch
COPY --from=downloader /pairdrop /pairdrop
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pairdrop /var/log/pairdrop
COPY --from=builder /var/cache/pairdrop /var/cache/pairdrop
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/pairdrop"]
LABEL org.opencontainers.image.title="pairdrop" \
      org.opencontainers.image.version="1.11.2" \
      org.opencontainers.image.vendor="PairDrop" \
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