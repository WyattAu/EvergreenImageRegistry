# =============================================================================
# SOVEREIGN HARDENED AUTOMATIC1111
# Generated from template - Version: 1.9.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.9.3
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 py3-pip git ca-certificates curl build-base
RUN git clone --depth 1 --branch v1.9.3 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/automatic1111 2>/dev/null || \
    git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /opt/automatic1111
RUN cd /opt/automatic1111 && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7860
ENTRYPOINT ["python3", "/opt/automatic1111/launch.py", "--listen", "--port", "7860"]
LABEL org.opencontainers.image.title="automatic1111" \
      org.opencontainers.image.version="1.9.3" \
      org.opencontainers.image.vendor="AUTOMATIC1111" \
      org.opencontainers.image.source="https://github.com/AUTOMATIC1111/stable-diffusion-webui.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM