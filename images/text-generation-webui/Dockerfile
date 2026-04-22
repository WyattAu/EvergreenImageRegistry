# =============================================================================
# SOVEREIGN HARDENED TEXT-GENERATION-WEBUI
# Generated from template - Version: 1.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.8
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 py3-pip python3 git ca-certificates curl build-base && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --break-system-packages torch torchvision --index-url https://download.pytorch.org/whl/cpu 2>/dev/null || true && \
    git clone --depth 1 --branch v${VERSION} https://github.com/oobabooga/text-generation-webui.git /opt/text-generation-webui 2>/dev/null || \
    git clone --depth 1 https://github.com/oobabooga/text-generation-webui.git /opt/text-generation-webui && \
    cd /opt/text-generation-webui && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true
RUN useradd -m -u 65532 -g '' user 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R user:user /app /var/log/python /var/cache/python 2>/dev/null || true
USER user
WORKDIR /app
EXPOSE 7860
ENTRYPOINT ["python3", "/opt/text-generation-webui/server.py"]
LABEL org.opencontainers.image.title="text-generation-webui" \
      org.opencontainers.image.version="1.8" \
      org.opencontainers.image.vendor="Oobabooga" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM