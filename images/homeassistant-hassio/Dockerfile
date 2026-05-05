
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant || true && \
    mkdir -p /config /data /app 2>/dev/null || true && \
    mkdir -p /opt/venv ; \
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

LABEL org.opencontainers.image.description="homeassistant-hassio container image" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervised-installer" \
            org.opencontainers.image.version="unknown"

ENTRYPOINT ["python", "-m", "homeassistant"]
CMD ["--help"]
