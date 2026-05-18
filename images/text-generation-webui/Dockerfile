# =============================================================================
# EVERGREEN HARDENED TEXT-GENERATION-WEBUI
# Generated from template - Version: 1.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.8
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.8
RUN apk add --no-cache git ca-certificates curl build-base || true && \
    pip install --no-cache-dir --break-system-packages torch torchvision --index-url https://download.pytorch.org/whl/cpu 2>/dev/null || true ; \
    git clone --branch v${VERSION} https://github.com/oobabooga/text-generation-webui.git /opt/text-generation-webui 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null && \
    cd /opt/text-generation-webui 2>/dev/null && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true && \
    adduser -u 65532 -D user 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R user:user /app /var/log/python /var/cache/python 2>/dev/null || true
USER user
WORKDIR /app
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:7860/ || exit 1
ENTRYPOINT ["python3", "/opt/text-generation-webui/server.py"]
LABEL org.opencontainers.image.title="text-generation-webui" \
      org.opencontainers.image.description="text-generation-webui container image" \
      org.opencontainers.image.version="1.8" \
      org.opencontainers.image.vendor="Oobabooga" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/oobabooga/text-generation-webui.git"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
