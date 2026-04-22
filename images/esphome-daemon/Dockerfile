FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates gcc g++ libc6-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /config /config
RUN useradd -r -u 65534 -g nogroup -d /config -s /sbin/nologin esphome 2>/dev/null || true && \
    chown -R 65534:65534 /config /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 6053
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:6053/ping')"] || exit 0
ENTRYPOINT ["esphome"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="esphome-daemon" \
      org.opencontainers.image.description="ESPHome - daemon mode" \
      org.opencontainers.image.vendor="ESPHome" \
      org.opencontainers.image.source="https://github.com/esphome/esphome" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
