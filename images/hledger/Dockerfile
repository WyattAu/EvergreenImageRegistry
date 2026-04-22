ARG VERSION=1.33
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/simonmichael/hledger/releases/download/1.33/hledger-1.33-linux-x86_64.tar.gz" -o /hledger.tar.gz && \
    tar -xzf /hledger.tar.gz -C /usr/local/bin/ && rm /hledger.tar.gz && \
    strip /usr/local/bin/hledger && chmod +x /usr/local/bin/hledger

FROM scratch
COPY --from=downloader /usr/local/bin/hledger /hledger
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/hledger", "--version"]
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
