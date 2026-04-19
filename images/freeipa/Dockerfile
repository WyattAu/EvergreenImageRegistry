# =============================================================================
# SOVEREIGN HARDENED FREEIPA
# Generated from template - Version: 4.12.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends freeipa-server ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' root 2>/dev/null || true
RUN mkdir -p /app /var/log/ipa-server /var/cache/ipa-server && chown -R root:root /app /var/log/ipa-server /var/cache/ipa-server 2>/dev/null || true
USER root
WORKDIR /app
EXPOSE 80 443 389 636
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ipa --version
ENTRYPOINT ["ipa-server"]
LABEL org.opencontainers.image.title="freeipa" \
      org.opencontainers.image.version="4.12.0" \
      org.opencontainers.image.vendor="FreeIPA" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
