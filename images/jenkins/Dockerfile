# =============================================================================
# SOVEREIGN HARDENED JENKINS
# Generated from template - Version: 2.462.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.462.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends default-jdk-headless ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' jenkins 2>/dev/null || true
RUN mkdir -p /app /var/log/jenkins /var/cache/jenkins && chown -R jenkins:jenkins /app /var/log/jenkins /var/cache/jenkins 2>/dev/null || true
USER jenkins
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD jenkins curl -s localhost:8080/api/json
ENTRYPOINT ["jenkins"]
LABEL org.opencontainers.image.title="jenkins" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
