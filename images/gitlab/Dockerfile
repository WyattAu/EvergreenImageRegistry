# =============================================================================
# SOVEREIGN HARDENED GITLAB
# Generated from template - Version: 16.12.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=16.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends gitlab-ce ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' git 2>/dev/null || true
RUN mkdir -p /app /var/log/gitlab-ce /var/cache/gitlab-ce && chown -R git:git /app /var/log/gitlab-ce /var/cache/gitlab-ce 2>/dev/null || true
USER git
WORKDIR /app
EXPOSE 80 22 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD gitlab-ce curl -s localhost:80/api/v4/health
ENTRYPOINT ["gitlab-ce"]
LABEL org.opencontainers.image.title="gitlab" \
      org.opencontainers.image.version="16.12.0" \
      org.opencontainers.image.vendor="GitLab" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
