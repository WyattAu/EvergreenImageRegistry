# =============================================================================
# SOVEREIGN HARDENED ADGUARDHOME-LITE
# AdGuard Home with minimal/lite config entrypoint
# Constraint: scratch - static Go binary
# =============================================================================

ARG VERSION=0.107.50
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/AdguardTeam/AdGuardHome/releases/download/v${VERSION}/AdGuardHome_linux_amd64.tar.gz" -o /AdGuardHome.tar.gz && \
    tar -xzf /AdGuardHome.tar.gz -C / && rm /AdGuardHome.tar.gz && \
    chmod +x /AdGuardHome && \
    strip --strip-all /AdGuardHome 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/AdGuardHome /var/cache/AdGuardHome /opt/AdGuardHome/data

FROM scratch
COPY --from=downloader /AdGuardHome /AdGuardHome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/AdGuardHome /var/log/AdGuardHome
COPY --from=builder /var/cache/AdGuardHome /var/cache/AdGuardHome
COPY --from=builder /opt/AdGuardHome/data /opt/AdGuardHome/data
USER 65534:65534
WORKDIR /app
EXPOSE 53 53/udp 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/AdGuardHome", "--version"]
ENTRYPOINT ["/AdGuardHome"]
CMD ["-c", "/opt/AdGuardHome/data/AdGuardHome.yaml", "--no-check-update"]
LABEL org.opencontainers.image.title="adguardhome-lite" \
      org.opencontainers.image.version="0.107.50" \
      org.opencontainers.image.vendor="AdGuard" \
      org.opencontainers.image.source="https://github.com/AdguardTeam/AdGuardHome" \
      org.opencontainers.image.description="AdGuard Home with lite/minimal config entrypoint" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
