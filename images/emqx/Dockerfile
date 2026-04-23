
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://www.emqx.com/en/downloads/broker/v5.8.0/emqx-5.8.0-debian12-amd64.tar.gz" \
    -o /emqx.tar.gz
RUN mkdir -p /opt/emqx && \
    tar -xzf /emqx.tar.gz -C /opt/emqx --strip-components=1 && rm /emqx.tar.gz
RUN mkdir -p /app /opt/emqx/data /opt/emqx/log


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl procps
COPY --from=builder /opt/emqx /opt/emqx
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /opt/emqx -s /sbin/nologin emqx 2>/dev/null || true && \
    chown -R 65532:65532 /opt/emqx /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/emqx
EXPOSE 1883 8083 8084 8883 18083
ENTRYPOINT ["/opt/emqx/bin/emqx"]
CMD ["foreground"]
LABEL org.opencontainers.image.title="emqx" \
      org.opencontainers.image.description="EMQX - High-performance MQTT broker" \
      org.opencontainers.image.vendor="EMQ" \
      org.opencontainers.image.source="https://github.com/emqx/emqx" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM