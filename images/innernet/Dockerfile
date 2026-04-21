# =============================================================================
# SOVEREIGN HARDENED INNERNET
# Private overlay network (server/peer daemon)
# Constraint: scratch - Rust static binary (musl), smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.16.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/innernet-rs/innernet/releases/download/v${VERSION}/innernet-${VERSION}-x86_64-unknown-linux-musl.tar.gz" -o /innernet.tar.gz && \
    mkdir -p /tmp/innernet && \
    tar -xzf /innernet.tar.gz -C /tmp/innernet && \
    strip --strip-all /tmp/innernet/innernet 2>/dev/null || true && \
    strip --strip-all /tmp/innernet/innernet-serve 2>/dev/null || true && \
    mv /tmp/innernet/innernet /innernet && \
    mv /tmp/innernet/innernet-serve /innernet-serve 2>/dev/null || true && \
    rm -rf /innernet.tar.gz /tmp/*

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/innernet

FROM scratch
COPY --from=downloader /innernet /innernet
COPY --from=downloader /innernet-serve /innernet-serve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/innernet /var/log/innernet
USER 65534:65534
WORKDIR /app
EXPOSE 51820/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/innernet", "--help"]
ENTRYPOINT ["/innernet"]
LABEL org.opencontainers.image.title="innernet" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="innernet-rs" \
      org.opencontainers.image.source="https://github.com/innernet-rs/innernet" \
      org.opencontainers.image.description="Private overlay network server (WireGuard-based)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
