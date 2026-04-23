# =============================================================================
# SOVEREIGN HARDENED GITHUB-ACTIONS-RUNNER
# Generated from template - Version: 2.316.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.316.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache curl git ca-certificates
RUN useradd -m -u 65532 -g '' runner 2>/dev/null || true
RUN mkdir -p /app /var/log/run.sh /var/cache/run.sh && chown -R runner:runner /app /var/log/run.sh /var/cache/run.sh 2>/dev/null || true
USER runner
WORKDIR /app
ENTRYPOINT ["run.sh"]
LABEL org.opencontainers.image.title="github-actions-runner" \
      org.opencontainers.image.version="2.316.1" \
      org.opencontainers.image.vendor="GitHub" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM