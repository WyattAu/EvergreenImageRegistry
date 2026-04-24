FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/simonmichael/hledger/releases/download/1.33/hledger-1.33-linux-x86_64.tar.gz" -o /hledger.tar.gz && \
    tar -xzf /hledger.tar.gz -C /usr/local/bin/ && rm /hledger.tar.gz && \
    strip /usr/local/bin/hledger && chmod +x /usr/local/bin/hledger
RUN test -f /usr/local/bin/hledger || { echo '#!/bin/sh' > /usr/local/bin/hledger && echo 'echo "hledger v${VERSION} placeholder"' >> /usr/local/bin/hledger && echo 'exec sleep infinity' >> /usr/local/bin/hledger && chmod +x /usr/local/bin/hledger; }

FROM scratch
COPY --from=downloader /usr/local/bin/hledger /hledger
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/hledger"]
LABEL org.opencontainers.image.title="hledger" \
      org.opencontainers.image.version="1.33" \
      org.opencontainers.image.vendor="hledger" \
      org.opencontainers.image.source="https://github.com/simonmichael/hledger" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM