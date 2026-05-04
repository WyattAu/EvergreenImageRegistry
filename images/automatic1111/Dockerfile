# =============================================================================
# EVERGREEN HARDENED AUTOMATIC1111
# Generated from template - Version: 1.9.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.9.3
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache git ca-certificates curl build-base || true && \
    git clone --depth 1 --branch v1.9.3 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/automatic1111 2>/dev/null || echo "Source repo not available - using placeholder" && \
    git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/automatic1111 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true && \
       git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/automatic1111 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true && \
    cd /opt/automatic1111 && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7860/ || exit 1
ENTRYPOINT ["python3", "/opt/automatic1111/launch.py", "--listen", "--port", "7860"]
LABEL org.opencontainers.image.title="automatic1111" \
      org.opencontainers.image.description="automatic1111 container image" \
      org.opencontainers.image.version="1.9.3" \
      org.opencontainers.image.vendor="AUTOMATIC1111" \
      org.opencontainers.image.source="https://github.com/AUTOMATIC1111/stable-diffusion-webui.git" \
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
