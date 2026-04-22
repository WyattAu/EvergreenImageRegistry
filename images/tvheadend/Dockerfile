# =============================================================================
# SOVEREIGN HARDENED TVHEADEND
# Generated from template - Version: 4.3
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -g '' hts 2>/dev/null || true
RUN mkdir -p /app /var/log/hts /var/cache/hts && chown -R hts:hts /app /var/log/hts /var/cache/hts 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9981
ENTRYPOINT ["tvheadend"]
LABEL org.opencontainers.image.title="tvheadend" \
      org.opencontainers.image.version="4.3" \
      org.opencontainers.image.vendor="TVHeadend" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM