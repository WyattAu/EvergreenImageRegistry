# =============================================================================
# SOVEREIGN HARDENED WANDB-SERVER
# Generated from template - Version: 0.19.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.19.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl || true
RUN pip install --no-cache-dir --break-system-packages wandb 2>/dev/null || \
    pip install --no-cache-dir wandb
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["wandb"]
LABEL org.opencontainers.image.title="wandb-server" \
      org.opencontainers.image.version="0.19.0" \
      org.opencontainers.image.vendor="Weights & Biases" \
      org.opencontainers.image.source="https://github.com/wandb/server" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM