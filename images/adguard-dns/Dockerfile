# =============================================================================
# SOVEREIGN HARDENED ADGUARD-DNS
# AdGuard Home DNS server
# Constraint: scratch - static Go binary
# =============================================================================

ARG VERSION=0.107.50
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/AdguardTeam/AdGuardHome/releases/download/v${VERSION}/AdGuardHome_linux_amd64.tar.gz" -o /AdGuardHome.tar.gz && \
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
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 3000 443 853
ENTRYPOINT ["/AdGuardHome"]
LABEL org.opencontainers.image.title="adguard-dns" \
      org.opencontainers.image.version="0.107.50" \
      org.opencontainers.image.vendor="AdGuard" \
      org.opencontainers.image.source="https://github.com/AdguardTeam/AdGuardHome" \
      org.opencontainers.image.description="AdGuard Home DNS server" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM