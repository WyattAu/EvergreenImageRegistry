# =============================================================================
# SOVEREIGN HARDENED SOFTETHER
# Generated from template - Version: 4.38-9770
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.38-9770
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends build-base ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/vpnserver /var/cache/vpnserver && chown -R appuser:appuser /app /var/log/vpnserver /var/cache/vpnserver 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 443 992 1194 500 4500 5555
ENTRYPOINT ["vpnserver"]
LABEL org.opencontainers.image.title="softether" \
      org.opencontainers.image.version="4.38-9770" \
      org.opencontainers.image.vendor="SoftEther" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM