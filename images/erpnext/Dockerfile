# =============================================================================
# SOVEREIGN HARDENED ERPNEXT
# Generated from template - Version: 15.11.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=15.11.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv redis-server ca-certificates curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' erpnext 2>/dev/null || true
RUN mkdir -p /app /var/log/erpnext /var/cache/erpnext && chown -R erpnext:erpnext /app /var/log/erpnext /var/cache/erpnext 2>/dev/null || true
USER erpnext
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="erpnext" \
      org.opencontainers.image.version="15.11.0" \
      org.opencontainers.image.vendor="ERPNext" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
