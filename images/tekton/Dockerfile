# =============================================================================
# SOVEREIGN HARDENED TEKTON
# Generated from template - Version: 0.61.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=0.61.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends tekton ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' tekton 2>/dev/null || true
RUN mkdir -p /app /var/log/tekton /var/cache/tekton && chown -R tekton:tekton /app /var/log/tekton /var/cache/tekton 2>/dev/null || true
USER tekton:tekton
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health
ENTRYPOINT ["tekton"]
LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.version="0.61.0" \
      org.opencontainers.image.vendor="Tekton" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
