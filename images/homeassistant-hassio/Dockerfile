
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN apk add --no-cache python3 py3-pip git ca-certificates curl && \
    python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate 2>/dev/null || true && \
    pip install --no-cache-dir --upgrade pip 2>/dev/null && \
    pip install --no-cache-dir homeassistant==2024.8.0 2>/dev/null && \
    mkdir -p /config /data /app /opt/venv 2>/dev/null || true
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
LABEL evergreen.base.image="wolfi"
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

LABEL org.opencontainers.image.description="homeassistant-hassio container image" \
      org.opencontainers.image.title="Home Assistant Hass.io Supervisor" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervised-installer" \
            org.opencontainers.image.version="unknown"

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python -m homeassistant"]
CMD ["--help"]
