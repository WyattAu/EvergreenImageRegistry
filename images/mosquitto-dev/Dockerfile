
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto mosquitto-clients ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true && \
    printf 'listener 1883\nallow_anonymous true\npersistence false\nlog_dest stderr\nlog_type all\n' > /app/mosquitto.conf
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache mosquitto mosquitto-clients ca-certificates curl || true
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false mosquitto 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 1883 9001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:1883/ || exit 1
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf", "-v"]
LABEL org.opencontainers.image.title="mosquitto-dev" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker - development mode" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
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
