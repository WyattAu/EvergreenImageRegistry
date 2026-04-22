ARG VERSION=0.65.22
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/airbyte-server /var/cache/airbyte-server /var/lib/airbyte

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/airbyte-server /var/log/airbyte-server
COPY --from=builder /var/cache/airbyte-server /var/cache/airbyte-server
COPY --from=builder /var/lib/airbyte /var/lib/airbyte
RUN useradd -r -u 65534 -g '' airbyte 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["java", "--version"]
ENTRYPOINT ["java", "-jar", "/app/server.jar"]
LABEL org.opencontainers.image.title="airbyte-server" \
      org.opencontainers.image.version="0.65.22" \
      org.opencontainers.image.vendor="Airbyte" \
      org.opencontainers.image.description="Sovereign hardened airbyte-server - Airbyte server process" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
