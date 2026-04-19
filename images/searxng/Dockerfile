# =============================================================================
# SOVEREIGN HARDENED SEARXNG
# Generated from template - Version: 2024.4.10
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.10
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-lxml ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' searxng 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R searxng:searxng /app /var/log/python /var/cache/python 2>/dev/null || true
USER searxng
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python curl -s localhost:8080/healthz
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="searxng" \
      org.opencontainers.image.version="2024.4.10" \
      org.opencontainers.image.vendor="SearXNG" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
