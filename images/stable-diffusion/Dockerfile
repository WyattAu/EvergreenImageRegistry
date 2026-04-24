# =============================================================================
# SOVEREIGN HARDENED STABLE-DIFFUSION
# Generated from template - Version: 2.1.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.1.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl
RUN pip3 install --no-cache-dir --break-system-packages diffusers transformers accelerate 2>/dev/null || \
    pip3 install --no-cache-dir diffusers transformers accelerate
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7860
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="stable-diffusion" \
      org.opencontainers.image.version="2.1.0" \
      org.opencontainers.image.vendor="Stability AI" \
      org.opencontainers.image.source="https://github.com/Stability-AI/stablediffusion" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM