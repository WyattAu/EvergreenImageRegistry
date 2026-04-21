# =============================================================================
# SOVEREIGN HARDENED SONIC
# Fast, lightweight search backend (Rust)
# Constraint: scratch - static Rust binary (best-effort)
# =============================================================================

ARG VERSION=1.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/valeriansaliou/sonic/releases/download/v${VERSION}/sonic-v${VERSION}-x86_64-linux-gnu.tar.gz" -o /sonic.tar.gz && \
    tar -xzf /sonic.tar.gz -C / && rm /sonic.tar.gz && \
    find / -maxdepth 2 -name "sonic" -type f -exec chmod +x {} \; && \
    strip --strip-all /sonic 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/sonic /var/lib/sonic /etc/sonic

FROM scratch
COPY --from=downloader /sonic /sonic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/sonic /var/log/sonic
COPY --from=builder /var/lib/sonic /var/lib/sonic
COPY --from=builder /etc/sonic /etc/sonic
USER 65534:65534
WORKDIR /app
EXPOSE 1491
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/sonic", "-v"]
ENTRYPOINT ["/sonic"]
LABEL org.opencontainers.image.title="sonic" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.vendor="valeriansaliou" \
      org.opencontainers.image.source="https://github.com/valeriansaliou/sonic" \
      org.opencontainers.image.description="Fast, lightweight search backend" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="best-effort" \
      sovereign.image.note="GNU binary may need glibc; fallback to debian-slim if scratch fails" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
