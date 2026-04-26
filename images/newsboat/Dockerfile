# =============================================================================
# SOVEREIGN HARDENED NEWSBOAT
# Generated from template - Version: 2.30
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.30
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D newsboat 2>/dev/null || true
RUN mkdir -p /app /var/log/newsboat /var/cache/newsboat && chown -R newsboat:newsboat /app /var/log/newsboat /var/cache/newsboat 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["newsboat"]
LABEL org.opencontainers.image.title="newsboat" \
      org.opencontainers.image.version="2.30" \
      org.opencontainers.image.vendor="Newsboat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM