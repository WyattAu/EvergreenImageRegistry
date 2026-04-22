# =============================================================================
# SOVEREIGN HARDENED JENKINS
# Generated from template - Version: 2.462.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.462.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends java-17 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' jenkins 2>/dev/null || true
RUN mkdir -p /app /var/log/jenkins /var/cache/jenkins && chown -R jenkins:jenkins /app /var/log/jenkins /var/cache/jenkins 2>/dev/null || true
USER jenkins
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["jenkins"]
LABEL org.opencontainers.image.title="jenkins" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM