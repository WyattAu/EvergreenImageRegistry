# =============================================================================
# SOVEREIGN HARDENED STABLE-DIFFUSION-WEBUI
# Generated from template - Version: 1.9.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.9.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git ca-certificates curl build-essential && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v1.9.3 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/stable-diffusion-webui 2>/dev/null || \
    git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/stable-diffusion-webui
RUN cd /opt/stable-diffusion-webui && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:7860/v1/models || exit 1
ENTRYPOINT ["python3", "/opt/stable-diffusion-webui/launch.py", "--listen", "--port", "7860"]
LABEL org.opencontainers.image.title="stable-diffusion-webui" \
      org.opencontainers.image.version="1.9.3" \
      org.opencontainers.image.vendor="AUTOMATIC1111" \
      org.opencontainers.image.source="https://github.com/AUTOMATIC1111/stable-diffusion-webui.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
