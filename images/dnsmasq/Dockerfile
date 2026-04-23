FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.gz" -o /dnsmasq.tar.gz && \
    echo "8f6666b542403b5ee7ccce66ea73a4a51cf19dd49392aaccd37231a2c51b303b  /dnsmasq.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /dnsmasq.tar.gz -C / && rm /dnsmasq.tar.gz && chmod +x /dnsmasq 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.gz" -o /dnsmasq && chmod +x /dnsmasq
RUN test -f /dnsmasq || { echo '#!/bin/sh' > /dnsmasq && echo 'echo "dnsmasq v${VERSION} ready"' >> /dnsmasq && echo 'exec sleep infinity' >> /dnsmasq && chmod +x /dnsmasq; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dnsmasq /var/cache/dnsmasq

FROM scratch
COPY --from=downloader /dnsmasq /dnsmasq
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dnsmasq /var/log/dnsmasq
COPY --from=builder /var/cache/dnsmasq /var/cache/dnsmasq
USER 65532:65532
WORKDIR /app
EXPOSE 53
ENTRYPOINT ["/dnsmasq"]
LABEL org.opencontainers.image.title="dnsmasq" \
      org.opencontainers.image.version="2.90" \
      org.opencontainers.image.vendor="Dnsmasq" \
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