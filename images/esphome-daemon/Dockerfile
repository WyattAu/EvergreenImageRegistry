







ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates gcc g++ libc6-dev ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true







ENV PATH="/opt/venv/bin:$PATH"







RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome==2024.8.0 
    mkdir -p /app /config







FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="Python C extensions require glibc"















RUN microdnf install -y python3 ca-certificates tzdata







COPY --from=builder /opt/venv /opt/venv







COPY --from=builder /app /app







COPY --from=builder /config /config







RUN addgroup -S nogroup || true && \
    adduser -u 65532 -G nogroup -D -h /config -s /bin/false esphome || true && \
    chown -R 65532:65532 /config /app







USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"







ENV PATH="/opt/venv/bin:$PATH" HOME="/config"







WORKDIR /config







EXPOSE 6053






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6053"]

ENTRYPOINT ["/shim", "run"]







CMD ["-c", "esphome", "--", "--daemon"]







LABEL org.opencontainers.image.title="esphome-daemon" \
      org.opencontainers.image.description="ESPHome - daemon mode" \
      org.opencontainers.image.vendor="ESPHome" \
      org.opencontainers.image.source="https://github.com/esphome/esphome" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
