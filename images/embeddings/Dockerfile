# =============================================================================
# SOVEREIGN HARDENED EMBEDDINGS
# Generated from template - Version: 0.1.0
# Constraint: debian-slim - placeholder awaiting upstream integration
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["true"]
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="embeddings" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Embeddings" \
      org.opencontainers.image.description="Placeholder - no upstream binary available" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
