
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update 2>/dev/null && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates curl 2>/dev/null ; rm -rf /var/lib/apt/lists/* 2>/dev/null || true && \
    python3 -m venv /opt/venv 2>/dev/null || true && \
    . /opt/venv/bin/activate 2>/dev/null || true && \
    pip install --no-cache-dir --upgrade pip 2>/dev/null || true && \
    pip install --no-cache-dir homeassistant==2024.8.0 2>/dev/null || true && \
    mkdir -p /config /data /app /opt/venv 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

LABEL org.opencontainers.image.description="homeassistant-hassio container image" \
      org.opencontainers.image.title="Home Assistant Hass.io Supervisor" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervised-installer" \
            org.opencontainers.image.version="unknown"

ENTRYPOINT ["python", "-m", "homeassistant"]
CMD ["--help"]
