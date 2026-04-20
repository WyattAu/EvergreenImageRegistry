# =============================================================================
# SOVEREIGN HARDENED TEXT-GENERATION-WEBUI
# Generated from template - Version: 1.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.8
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git ca-certificates curl && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir text-generation-webui==${VERSION} 2>/dev/null || \
    pip3 install --no-cache-dir git+https://github.com/oobabooga/text-generation-webui.git@v${VERSION}
RUN useradd -m -u 65534 -g '' user 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R user:user /app /var/log/python /var/cache/python 2>/dev/null || true
USER user
WORKDIR /app
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:7860/v1/models
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="text-generation-webui" \
      org.opencontainers.image.version="1.8" \
      org.opencontainers.image.vendor="Oobabooga" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
