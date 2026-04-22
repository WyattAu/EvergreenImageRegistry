# =============================================================================
# SOVEREIGN HARDENED LOCALAI-CUDA
# Generated from template - Version: 2.30.0
# Constraint: debian-slim - placeholder awaiting upstream integration
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.30.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="localai-cuda" \
      org.opencontainers.image.version="2.30.0" \
      org.opencontainers.image.vendor="LocalAI" \
      org.opencontainers.image.description="GPU placeholder - requires NVIDIA CUDA runtime" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM