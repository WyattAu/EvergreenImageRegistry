# =============================================================================
# SOVEREIGN HARDENED PYTORCH-CUDA
# Generated from template - Version: 2.6.0
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.6.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl
RUN adduser -u 65532 -G '' -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="pytorch-cuda" \
      org.opencontainers.image.version="2.6.0" \
      org.opencontainers.image.vendor="PyTorch" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM