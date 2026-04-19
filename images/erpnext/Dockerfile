# =============================================================================
# SOVEREIGN HARDENED ERPNEXT
# Generated from template - Version: 15.11.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=15.11.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 py3-pip redis ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' erpnext 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R erpnext:erpnext /app /var/log/python /var/cache/python 2>/dev/null || true
USER erpnext
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python curl localhost:8000
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="erpnext" \
      org.opencontainers.image.version="15.11.0" \
      org.opencontainers.image.vendor="ERPNext" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
