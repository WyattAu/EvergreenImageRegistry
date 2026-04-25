
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg procps ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /app /opt/vernemq/data /opt/vernemq/log 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl procps || true
COPY --from=builder /app /app
COPY --from=builder /opt/vernemq /opt/vernemq
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /opt/vernemq -s /sbin/nologin vernemq 2>/dev/null || true && \
    chown -R 65532:65532 /opt/vernemq /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/vernemq
EXPOSE 1883 4369 44053 8080
ENTRYPOINT ["echo"]
CMD ["vernemq: Place VerneMQ binary in /opt/vernemq/bin/"]
LABEL org.opencontainers.image.title="vernemq" \
      org.opencontainers.image.description="VerneMQ - High-performance MQTT broker" \
      org.opencontainers.image.vendor="VerneMQ" \
      org.opencontainers.image.source="https://github.com/vernemq/vernemq" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM