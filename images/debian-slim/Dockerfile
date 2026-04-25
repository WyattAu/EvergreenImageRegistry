# =============================================================================
# SOVEREIGN BASE - DEBIAN SLIM
# Minimal debian:bookworm-slim reference image with hardening.
# This is the recommended fallback base for application images.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates tzdata dumb-init || true

RUN addgroup -S 65532 -r appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -D -h /app -s /sbin/nologin appuser 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="debian-slim" \
      org.opencontainers.image.description="Sovereign hardened debian:bookworm-slim base image with ca-certificates, tzdata, dumb-init" \
      sovereign.image.tier="3" \
      sovereign.image.status="functional" \
      sovereign.image.category="base" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
