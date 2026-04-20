# =============================================================================
# SOVEREIGN HARDENED FAIL2BAN
# Generated from template - Version: 1.0.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends fail2ban ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/fail2ban /var/cache/fail2ban && chown -R appuser:appuser /app /var/log/fail2ban /var/cache/fail2ban 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD fail2ban-client status
ENTRYPOINT ["fail2ban"]
LABEL org.opencontainers.image.title="fail2ban" \
      org.opencontainers.image.version="1.0.2" \
      org.opencontainers.image.vendor="Fail2Ban" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
