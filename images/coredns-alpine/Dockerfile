# =============================================================================
# SOVEREIGN HARDENED COREDNS-ALPINE
# CoreDNS DNS server (alpine variant name, built on scratch)
# Constraint: scratch - Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Alpine is BANNED - using scratch with debian-slim downloader
# =============================================================================

ARG VERSION=1.11.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/coredns/coredns/releases/download/v${VERSION}/coredns_${VERSION}_linux_amd64.tgz" -o /coredns.tar.gz && \
    mkdir -p /tmp/coredns && \
    tar -xzf /coredns.tar.gz -C /tmp/coredns && \
    strip --strip-all /tmp/coredns/coredns && \
    mv /tmp/coredns/coredns /coredns && \
    rm -rf /coredns.tar.gz /tmp/*

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/coredns /var/cache/coredns

FROM scratch
COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/coredns /var/log/coredns
COPY --from=builder /var/cache/coredns /var/cache/coredns
USER 65534:65534
WORKDIR /app
EXPOSE 53 53/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/coredns", "-version"]
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns-alpine" \
      org.opencontainers.image.version="1.11.1" \
      org.opencontainers.image.vendor="CoreDNS" \
      org.opencontainers.image.source="https://github.com/coredns/coredns" \
      org.opencontainers.image.description="CoreDNS DNS server (alpine variant, built without Alpine)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
