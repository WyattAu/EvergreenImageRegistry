# =============================================================================
# SOVEREIGN HARDENED COMFYUI
# Generated from template - Version: latest
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache git ca-certificates curl build-essential
RUN git clone --depth 1 --branch vlatest https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || echo "Source repo not available - using placeholder" && \
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || trueRUN cd /opt/comfyui && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8188
ENTRYPOINT ["python3", "/opt/comfyui/main.py", "--listen", "--port", "8188"]
LABEL org.opencontainers.image.title="comfyui" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="ComfyUI" \
      org.opencontainers.image.source="https://github.com/comfyanonymous/ComfyUI.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
