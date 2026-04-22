FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant
RUN mkdir -p /config /data /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata dbus libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin hass 2>/dev/null || true && \
    mkdir -p /config /data && chown -R 65534:65534 /config /data /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config" HASSIO="1"
WORKDIR /config
EXPOSE 8123
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/opt/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8123/api/')"]
ENTRYPOINT ["/opt/venv/bin/hass"]
CMD ["--config", "/config"]
LABEL org.opencontainers.image.title="homeassistant-hassio" \
      org.opencontainers.image.description="Home Assistant in HassIO mode" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/core" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
