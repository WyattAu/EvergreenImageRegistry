FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.emqx.com/en/downloads/broker/v5.8.0/emqx-5.8.0-debian12-amd64.tar.gz" \
    -o /emqx.tar.gz
RUN mkdir -p /opt/emqx && \
    tar -xzf /emqx.tar.gz -C /opt/emqx --strip-components=1 && rm /emqx.tar.gz
RUN mkdir -p /app /opt/emqx/data /opt/emqx/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libodbc1 libssl3 ca-certificates curl procps \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/emqx /opt/emqx
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/emqx -s /sbin/nologin emqx 2>/dev/null || true && \
    chown -R 65534:65534 /opt/emqx /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:18083/api/v5/status"]
ENTRYPOINT ["/opt/emqx/bin/emqx"]
CMD ["foreground"]
LABEL org.opencontainers.image.title="emqx" \
      org.opencontainers.image.description="EMQX - High-performance MQTT broker" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
