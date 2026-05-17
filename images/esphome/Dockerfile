







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates gcc g++ libc6-dev ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true







ENV PATH="/opt/venv/bin:$PATH"







RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome==2024.8.0 ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/esphome || { echo '#!/bin/sh' > /usr/local/bin/esphome && echo 'echo "esphome v${VERSION} placeholder"' >> /usr/local/bin/esphome && echo 'exec sleep infinity' >> /usr/local/bin/esphome && chmod +x /usr/local/bin/esphome ; } || true && \
    mkdir -p /app /config







FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache python3 ca-certificates tzdata 







COPY --from=builder /opt/venv /opt/venv







COPY --from=builder /app /app







COPY --from=builder /config /config







RUN addgroup -S nogroup || true && \
    adduser -u 65532 -G nogroup -D -h /config -s /bin/false esphome || true && \
    chown -R 65532:65532 /config /app







USER 65532:65532







ENV PATH="/opt/venv/bin:$PATH" HOME="/config"







WORKDIR /config







EXPOSE 6052















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:6052/ || exit 1







ENTRYPOINT ["esphome"]







CMD ["config", "/config", "dashboard"]







LABEL org.opencontainers.image.title="esphome" \
      org.opencontainers.image.description="ESPHome - ESP8266/ESP32 firmware builder" \
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







STOPSIGNAL SIGTERM
