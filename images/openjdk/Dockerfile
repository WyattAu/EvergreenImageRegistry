# =============================================================================
# SOVEREIGN HARDENED OPENJDK
# Generated from template - Version: 21.0.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=21.0.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk21 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' java 2>/dev/null || true
RUN mkdir -p /app /var/log/java /var/cache/java && chown -R java:java /app /var/log/java /var/cache/java 2>/dev/null || true
USER java
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD java java -version
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk" \
      org.opencontainers.image.version="21.0.3" \
      org.opencontainers.image.vendor="OpenJDK" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
