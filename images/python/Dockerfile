# =============================================================================
# SOVEREIGN HARDENED PYTHON
# Generated from template - Version: 3.12.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.12.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' python 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R python:python /app /var/log/python /var/cache/python 2>/dev/null || true
USER python
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python python --version
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="python" \
      org.opencontainers.image.version="3.12.3" \
      org.opencontainers.image.vendor="Python" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
