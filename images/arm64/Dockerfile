# =============================================================================

# SOVEREIGN REFERENCE - ARM64 MULTI-ARCH

# Multi-architecture reference image for arm64/aarch64 targets.

# =============================================================================

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates tzdata || true
LABEL org.opencontainers.image.title="arm64" \
      org.opencontainers.image.description="Sovereign multi-arch reference for arm64/aarch64 platform" \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Multi-architecture reference image. Build with docker buildx --platform linux/arm64." \
      sovereign.base.image="wolfi" \
      sovereign.metrics.native="ztunnel" \
      sovereign.health.type="none"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM
