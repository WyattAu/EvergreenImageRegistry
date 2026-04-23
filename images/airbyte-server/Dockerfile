ARG VERSION=0.65.22
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-base && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/airbyte-server /var/cache/airbyte-server /var/lib/airbyte


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/airbyte-server /var/log/airbyte-server
COPY --from=builder /var/cache/airbyte-server /var/cache/airbyte-server
COPY --from=builder /var/lib/airbyte /var/lib/airbyte
RUN adduser -u 65532 -G '' -D airbyte 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
EXPOSE 8000
ENTRYPOINT ["java", "-jar", "/app/server.jar"]
LABEL org.opencontainers.image.title="airbyte-server" \
      org.opencontainers.image.version="0.65.22" \
      org.opencontainers.image.vendor="Airbyte" \
      org.opencontainers.image.description="Sovereign hardened airbyte-server - Airbyte server process" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM