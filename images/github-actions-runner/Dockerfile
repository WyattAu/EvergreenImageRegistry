# =============================================================================
# SOVEREIGN HARDENED GITHUB-ACTIONS-RUNNER
# Generated from template - Version: 2.316.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.316.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl git ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' runner 2>/dev/null || true
RUN mkdir -p /app /var/log/run.sh /var/cache/run.sh && chown -R runner:runner /app /var/log/run.sh /var/cache/run.sh 2>/dev/null || true
USER runner
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ./run.sh --version
ENTRYPOINT ["run.sh"]
LABEL org.opencontainers.image.title="github-actions-runner" \
      org.opencontainers.image.version="2.316.1" \
      org.opencontainers.image.vendor="GitHub" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
