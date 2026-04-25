
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates \
    && rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
RUN printf 'listener 1883\nallow_anonymous false\npersistence false\nlog_dest stderr\n' > /app/mosquitto.conf


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache mosquitto ca-certificates || true
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 1883 9001
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf"]
LABEL org.opencontainers.image.title="mosquitto" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM