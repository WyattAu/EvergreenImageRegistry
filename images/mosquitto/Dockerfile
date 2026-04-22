FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/mosquitto /var/lib/mosquitto
RUN printf 'listener 1883\nallow_anonymous false\npersistence false\nlog_dest stderr\n' > /app/mosquitto.conf

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/mosquitto /var/log/mosquitto
COPY --from=builder /var/lib/mosquitto /var/lib/mosquitto
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/mosquitto /var/lib/mosquitto 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 1883 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"] || exit 0
ENTRYPOINT ["mosquitto"]
CMD ["-c", "/app/mosquitto.conf"]
LABEL org.opencontainers.image.title="mosquitto" \
      org.opencontainers.image.description="Eclipse Mosquitto MQTT broker" \
      org.opencontainers.image.vendor="Eclipse" \
      org.opencontainers.image.source="https://github.com/eclipse/mosquitto" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
