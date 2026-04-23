# =============================================================================
# SOVEREIGN HARDENED CALIBRE-WEB
# Generated from template - Version: 0.6.22
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.6.22
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3-pip ca-certificates
RUN adduser -u 65532 -G '' -D calibre 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R calibre:calibre /app /var/log/python /var/cache/python 2>/dev/null || true
USER calibre
WORKDIR /app
EXPOSE 8083
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="calibre-web" \
      org.opencontainers.image.version="0.6.22" \
      org.opencontainers.image.vendor="Calibre-Web" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM