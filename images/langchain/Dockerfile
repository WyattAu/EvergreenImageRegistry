# =============================================================================
# SOVEREIGN HARDENED LANGCHAIN
# Generated from template - Version: 0.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv ca-certificates curl  \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --break-system-packages langchain 2>/dev/null || \
    pip3 install --no-cache-dir langchain
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "--version"]
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="langchain" \
      org.opencontainers.image.version="0.3.0" \
      org.opencontainers.image.vendor="LangChain" \
      org.opencontainers.image.source="https://github.com/langchain-ai/langchain" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
