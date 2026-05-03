# =============================================================================
# SOVEREIGN HARDENED ERPNEXT
# Generated from template - Version: 15.11.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=15.11.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D erpnext 2>/dev/null || true
RUN mkdir -p /app /var/log/erpnext /var/cache/erpnext && chown -R erpnext:erpnext /app /var/log/erpnext /var/cache/erpnext 2>/dev/null || true
USER erpnext
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="erpnext" \
      org.opencontainers.image.version="15.11.0" \
      org.opencontainers.image.vendor="ERPNext" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
