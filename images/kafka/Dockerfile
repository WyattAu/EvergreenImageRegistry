# =============================================================================
# SOVEREIGN HARDENED KAFKA
# Generated from template - Version: 3.7.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.7.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk17 kafka ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' kafka 2>/dev/null || true
RUN mkdir -p /app /var/log/kafka /var/cache/kafka && chown -R kafka:kafka /app /var/log/kafka /var/cache/kafka 2>/dev/null || true
USER kafka
WORKDIR /app
EXPOSE 9092
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD kafka kafka-broker-api-versions --version
ENTRYPOINT ["kafka"]
LABEL org.opencontainers.image.title="kafka" \
      org.opencontainers.image.version="3.7.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
