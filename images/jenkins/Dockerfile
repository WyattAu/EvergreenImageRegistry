# =============================================================================
# SOVEREIGN HARDENED JENKINS
# Generated from template - Version: 2.462
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.462
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends jenkins ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' jenkins 2>/dev/null || true
RUN mkdir -p /app /var/log/jenkins /var/cache/jenkins && chown -R jenkins:jenkins /app /var/log/jenkins /var/cache/jenkins 2>/dev/null || true
USER jenkins:jenkins
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/json
ENTRYPOINT ["jenkins"]
LABEL org.opencontainers.image.title="jenkins" \
      org.opencontainers.image.version="2.462" \
      org.opencontainers.image.vendor="Jenkins" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
