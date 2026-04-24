# =============================================================================
# SOVEREIGN HARDENED IMMICH
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache nodejs ffmpeg ca-certificates
RUN adduser -u 65532 -D immich 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R immich:immich /app /var/log/node /var/cache/node 2>/dev/null || true
USER immich
WORKDIR /app
EXPOSE 2283
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="immich" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM