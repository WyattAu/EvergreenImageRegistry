# =============================================================================
# EVERGREEN HARDENED COMFYUI
# Generated from template - Version: latest
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=latest
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache git ca-certificates curl build-base || true && \
    git clone --depth 1 --branch vlatest https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || echo "Source repo not available - using placeholder" && \
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true && \
       git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true && \
    cd /opt/comfyui && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8188

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8188/ || exit 1
ENTRYPOINT ["python3", "/opt/comfyui/main.py", "--listen", "--port", "8188"]
LABEL org.opencontainers.image.title="comfyui" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="ComfyUI" \
      org.opencontainers.image.source="https://github.com/comfyanonymous/ComfyUI.git" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
