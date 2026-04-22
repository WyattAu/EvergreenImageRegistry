# =============================================================================
# SOVEREIGN HARDENED NEWSBOAT
# Generated from template - Version: 2.30
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.30
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    newsboat ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' newsboat 2>/dev/null || true
RUN mkdir -p /app /var/log/newsboat /var/cache/newsboat && chown -R newsboat:newsboat /app /var/log/newsboat /var/cache/newsboat 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["newsboat", "--version"]
ENTRYPOINT ["newsboat"]
LABEL org.opencontainers.image.title="newsboat" \
      org.opencontainers.image.version="2.30" \
      org.opencontainers.image.vendor="Newsboat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
