# =============================================================================
# SOVEREIGN HARDENED GITEA
# Generated from template - Version: 1.21.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends gitea ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' git 2>/dev/null || true
RUN mkdir -p /app /var/log/gitea /var/cache/gitea && chown -R git:git /app /var/log/gitea /var/cache/gitea 2>/dev/null || true
USER git:git
WORKDIR /app
EXPOSE 3000 22
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/health
ENTRYPOINT ["gitea"]
LABEL org.opencontainers.image.title="gitea" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="Gitea" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
