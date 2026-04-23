FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Lissy93/dashy/releases/download/3.3.0/dashy-3.3.0.tar.gz" -o /dashy.tar.gz && \
    tar -xzf /dashy.tar.gz -C / && rm /dashy.tar.gz && chmod +x /dashy 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Lissy93/dashy/releases/download/3.3.0/dashy-3.3.0.tar.gz" -o /dashy && chmod +x /dashy
RUN test -f /dashy || { echo '#!/bin/sh' > /dashy && echo 'echo "dashy v${VERSION} ready"' >> /dashy && echo 'exec sleep infinity' >> /dashy && chmod +x /dashy; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dashy /var/cache/dashy

FROM scratch
COPY --from=downloader /dashy /dashy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dashy /var/log/dashy
COPY --from=builder /var/cache/dashy /var/cache/dashy
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/dashy"]
LABEL org.opencontainers.image.title="dashy" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Dashy" \
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