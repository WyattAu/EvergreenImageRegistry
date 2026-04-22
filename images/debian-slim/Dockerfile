# =============================================================================
# SOVEREIGN BASE - DEBIAN SLIM
# Minimal debian:bookworm-slim reference image with hardening.
# This is the recommended fallback base for application images.
# =============================================================================

FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates tzdata dumb-init && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN groupadd -g 65534 -r appuser 2>/dev/null || true && \
    useradd -r -u 65534 -g appuser -d /app -s /sbin/nologin appuser 2>/dev/null || true

USER 65534:65534
WORKDIR /app

LABEL org.opencontainers.image.title="debian-slim" \
      org.opencontainers.image.description="Sovereign hardened debian:bookworm-slim base image with ca-certificates, tzdata, dumb-init" \
      sovereign.image.tier="3" \
      sovereign.image.status="functional" \
      sovereign.image.category="base" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
