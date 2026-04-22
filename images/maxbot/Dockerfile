# =============================================================================
# SOVEREIGN HARDENED MAXBOT
# Generated from template - Version: 0.1.0
# Constraint: debian-slim - placeholder awaiting upstream integration
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.1.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="maxbot" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="MaxBot" \
      org.opencontainers.image.description="Placeholder - no upstream binary available" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM