# =============================================================================
# SOVEREIGN HARDENED FAIL2BAN
# Generated from template - Version: 1.0.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -D appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/fail2ban /var/cache/fail2ban && chown -R appuser:appuser /app /var/log/fail2ban /var/cache/fail2ban 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 22
ENTRYPOINT ["fail2ban"]
LABEL org.opencontainers.image.title="fail2ban" \
      org.opencontainers.image.version="1.0.2" \
      org.opencontainers.image.vendor="Fail2Ban" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM