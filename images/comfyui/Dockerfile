# =============================================================================
# SOVEREIGN HARDENED COMFYUI
# Generated from template - Version: latest
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git ca-certificates curl build-essential && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch vlatest https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || \
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui
RUN cd /opt/comfyui && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8188
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8188/system_stats || exit 1
ENTRYPOINT ["python3", "/opt/comfyui/main.py", "--listen", "--port", "8188"]
LABEL org.opencontainers.image.title="comfyui" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="ComfyUI" \
      org.opencontainers.image.source="https://github.com/comfyanonymous/ComfyUI.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
