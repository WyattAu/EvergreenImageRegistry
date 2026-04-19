# =============================================================================
# SOVEREIGN HARDENED FORGEJO
# Generated from template - Version: 1.0.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi not available
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends forgejo ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' git 2>/dev/null || true
RUN mkdir -p /app /var/log/forgejo /var/cache/forgejo && chown -R git:git /app /var/log/forgejo /var/cache/forgejo 2>/dev/null || true
USER git:git
WORKDIR /app
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/health
ENTRYPOINT ["forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Forgejo" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
