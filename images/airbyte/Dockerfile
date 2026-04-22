ARG VERSION=0.65.22
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates java-17-runtime && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/airbyte /var/cache/airbyte /var/lib/airbyte

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/airbyte /var/log/airbyte
COPY --from=builder /var/cache/airbyte /var/cache/airbyte
COPY --from=builder /var/lib/airbyte /var/lib/airbyte
RUN useradd -r -u 65532 -g '' airbyte 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["java", "-jar", "/app/airbyte.jar"]
LABEL org.opencontainers.image.title="airbyte" \
      org.opencontainers.image.version="0.65.22" \
      org.opencontainers.image.vendor="Airbyte" \
      org.opencontainers.image.description="Sovereign hardened airbyte - ELT platform" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM