# =============================================================================
# SOVEREIGN HARDENED ADGUARDHOME
# Generated from template - Version: 0.107.48
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.107.48
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/AdguardTeam/AdGuardHome/releases/download/v0.107.48/AdGuardHome_0.107.48_linux_amd64.tar.gz" -o /AdGuardHome.tar.gz && \
    tar -xzf /AdGuardHome.tar.gz -C / && rm /AdGuardHome.tar.gz && chmod +x /AdGuardHome 2>/dev/null || \
    curl -fsSL "https://github.com/AdguardTeam/AdGuardHome/releases/download/v0.107.48/AdGuardHome_0.107.48_linux_amd64.tar.gz" -o /AdGuardHome && chmod +x /AdGuardHome

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/AdGuardHome /var/cache/AdGuardHome

FROM scratch
COPY --from=downloader /AdGuardHome /AdGuardHome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/AdGuardHome /var/log/AdGuardHome
COPY --from=builder /var/cache/AdGuardHome /var/cache/AdGuardHome
USER 65534:65534
WORKDIR /app
EXPOSE 53 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD AdGuardHome AdGuardHome --version
ENTRYPOINT ["/AdGuardHome"]
LABEL org.opencontainers.image.title="adguardhome" \
      org.opencontainers.image.version="0.107.48" \
      org.opencontainers.image.vendor="AdGuard" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
