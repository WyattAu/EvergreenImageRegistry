# =============================================================================
# SOVEREIGN HARDENED TEKTON
# Generated from template - Version: 0.61.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.61.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends tekton ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' tekton 2>/dev/null || true
RUN mkdir -p /app /var/log/tekton /var/cache/tekton && chown -R tekton:tekton /app /var/log/tekton /var/cache/tekton 2>/dev/null || true
USER tekton
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD tekton tkn --version
ENTRYPOINT ["tekton"]
LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.version="0.61.0" \
      org.opencontainers.image.vendor="Tekton" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
