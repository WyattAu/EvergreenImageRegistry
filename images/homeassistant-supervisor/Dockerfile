FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl jq \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir git+https://github.com/home-assistant/supervisor.git@main
RUN mkdir -p /data /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata dbus curl jq \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /data -s /sbin/nologin supervisor 2>/dev/null || true && \
    mkdir -p /data && chown -R 65534:65534 /data /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH" HOME="/data" SUPERVISOR="1"
WORKDIR /data
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/opt/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:80/supervisor/info')"] || exit 0
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["-m", "supervisor"]
LABEL org.opencontainers.image.title="homeassistant-supervisor" \
      org.opencontainers.image.description="Home Assistant Supervisor - manages add-ons" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervisor" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
