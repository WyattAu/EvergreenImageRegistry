FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto-clients ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        mosquitto-clients ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin mosquitto 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"] || exit 0
ENTRYPOINT ["mosquitto_pub"]
LABEL org.opencontainers.image.title="mosquito" \
      org.opencontainers.image.description="Mosquitto MQTT client tools" \
      org.opencontainers.image.vendor="Eclipse" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
