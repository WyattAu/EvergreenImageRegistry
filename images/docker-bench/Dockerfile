
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/docker/docker-bench-security.git /src 2>/dev/null || echo "Source repo not available - using placeholder"
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin bench 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
ENTRYPOINT ["sh"]
CMD ["docker-bench-security.sh"]
LABEL org.opencontainers.image.title="docker-bench" \
      org.opencontainers.image.description="Docker Bench for Security" \
      org.opencontainers.image.vendor="Docker" \
      org.opencontainers.image.source="https://github.com/docker/docker-bench-security" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM