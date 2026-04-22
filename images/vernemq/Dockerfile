FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg procps \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /opt/vernemq/data /opt/vernemq/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libssl3 ca-certificates curl procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /opt/vernemq /opt/vernemq
RUN useradd -r -u 65534 -g nogroup -d /opt/vernemq -s /sbin/nologin vernemq 2>/dev/null || true && \
    chown -R 65534:65534 /opt/vernemq /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/vernemq
EXPOSE 1883 4369 44053 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/api/v1/health"] || exit 0
ENTRYPOINT ["echo"]
CMD ["vernemq: Place VerneMQ binary in /opt/vernemq/bin/"]
LABEL org.opencontainers.image.title="vernemq" \
      org.opencontainers.image.description="VerneMQ - High-performance MQTT broker" \
      org.opencontainers.image.vendor="VerneMQ" \
      org.opencontainers.image.source="https://github.com/vernemq/vernemq" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
