# =============================================================================
# SOVEREIGN HARDENED POWERDNS
# Generated from template - Version: 4.9.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.9.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends pdns-server pdns-recursor ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/pdns /var/cache/pdns && chown -R appuser:appuser /app /var/log/pdns /var/cache/pdns 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 53 8081
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pdns_control ping
ENTRYPOINT ["pdns"]
LABEL org.opencontainers.image.title="powerdns" \
      org.opencontainers.image.version="4.9.1" \
      org.opencontainers.image.vendor="PowerDNS" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
