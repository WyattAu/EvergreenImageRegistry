# =============================================================================
# SOVEREIGN HARDENED TRANSMISSION
# Generated from template - Version: 4.0.6
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.6
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -G '' -D transmission 2>/dev/null || true
RUN mkdir -p /app /var/log/transmission-daemon /var/cache/transmission-daemon && chown -R transmission:transmission /app /var/log/transmission-daemon /var/cache/transmission-daemon 2>/dev/null || true
USER transmission
WORKDIR /app
EXPOSE 9091
ENTRYPOINT ["transmission-daemon"]
LABEL org.opencontainers.image.title="transmission" \
      org.opencontainers.image.version="4.0.6" \
      org.opencontainers.image.vendor="Transmission" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM