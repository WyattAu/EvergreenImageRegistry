ARG VERSION=v3.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/loki/releases/download/v3.1.0/loki-linux-amd64.zip" -o /loki.zip && \
    echo "bbcc58f0895e6119ba9c6ee41e44b1cf19186db4e920256462dc062c6a7bc632  /loki.zip" | sha256sum -c - && \
    unzip /loki.zip -d /tmp/loki && rm /loki.zip && mv /tmp/loki/loki-linux-amd64 /loki && chmod +x /loki && strip /loki

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/loki-simple /var/cache/loki-simple /etc/loki

FROM scratch
COPY --from=downloader /loki /loki
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki-simple /var/log/loki-simple
COPY --from=builder /var/cache/loki-simple /var/cache/loki-simple
COPY --from=builder /etc/loki /etc/loki
USER 65534:65534
WORKDIR /app
EXPOSE 3100
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/loki", "--version"]
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
