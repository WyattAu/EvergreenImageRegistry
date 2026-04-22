# =============================================================================
# SOVEREIGN HARDENED TVHEADEND
# Generated from template - Version: 4.3
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    tvheadend ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' hts 2>/dev/null || true
RUN mkdir -p /app /var/log/hts /var/cache/hts && chown -R hts:hts /app /var/log/hts /var/cache/hts 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9981
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:9981/ || exit 1
ENTRYPOINT ["tvheadend"]
LABEL org.opencontainers.image.title="tvheadend" \
      org.opencontainers.image.version="4.3" \
      org.opencontainers.image.vendor="TVHeadend" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
