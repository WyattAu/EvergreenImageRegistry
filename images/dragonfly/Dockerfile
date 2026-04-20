# =============================================================================
# SOVEREIGN HARDENED DRAGONFLY
# Generated from template - Version: 1.21.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dragonflydb/dragonfly/releases/download/v${VERSION}/dragonfly-x86_64.tar.gz" -o /tmp/dragonfly.tar.gz && \
    tar -xzf /tmp/dragonfly.tar.gz -C /usr/local/bin && rm /tmp/dragonfly.tar.gz && \
    chmod +x /usr/local/bin/dragonfly
RUN useradd -m -u 65534 -g '' dragonfly 2>/dev/null || true
RUN mkdir -p /app /var/log/dragonfly /var/cache/dragonfly && chown -R dragonfly:dragonfly /app /var/log/dragonfly /var/cache/dragonfly 2>/dev/null || true
USER dragonfly
WORKDIR /app
EXPOSE 6379 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000
ENTRYPOINT ["dragonfly"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
