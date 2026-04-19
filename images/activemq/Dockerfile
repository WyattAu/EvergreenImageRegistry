# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ
# Generated from template - Version: 6.1.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=6.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends activemq ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' activemq 2>/dev/null || true
RUN mkdir -p /app /var/log/activemq /var/cache/activemq && chown -R activemq:activemq /app /var/log/activemq /var/cache/activemq 2>/dev/null || true
USER activemq:activemq
WORKDIR /app
EXPOSE 61616 8161
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD activemq status
ENTRYPOINT ["activemq"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="6.1.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
