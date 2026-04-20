# =============================================================================
# SOVEREIGN HARDENED PHOTOPRISM
# Generated from template - Version: 240427
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=240427
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.photoprism.app/pkg/linux-amd64/photoprism-${VERSION}-linux-amd64.tar.gz" -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /opt && rm /tmp/photoprism.tar.gz && \
    chmod +x /opt/photoprism 2>/dev/null || true
RUN useradd -m -u 65534 -g '' photoprism 2>/dev/null || true
RUN mkdir -p /app /var/log/photoprism /var/cache/photoprism && chown -R photoprism:photoprism /app /var/log/photoprism /var/cache/photoprism /opt/photoprism 2>/dev/null || true
USER photoprism
WORKDIR /app
EXPOSE 2282
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:2282/api/v1/status
ENTRYPOINT ["/opt/photoprism"]
LABEL org.opencontainers.image.title="photoprism" \
      org.opencontainers.image.version="240427" \
      org.opencontainers.image.vendor="PhotoPrism" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
