# =============================================================================
# SOVEREIGN HARDENED CALIBRE-WEB
# Generated from template - Version: 0.6.22
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.6.22
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' calibre 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R calibre:calibre /app /var/log/python /var/cache/python 2>/dev/null || true
USER calibre
WORKDIR /app
EXPOSE 8083
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python curl -s localhost:8083/api/status
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="calibre-web" \
      org.opencontainers.image.version="0.6.22" \
      org.opencontainers.image.vendor="Calibre-Web" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
