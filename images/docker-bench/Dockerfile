FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/docker/docker-bench-security.git /src
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin bench 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["sh", "/app/src/docker-bench-security.sh", "--help"] || exit 0
ENTRYPOINT ["sh"]
CMD ["docker-bench-security.sh"]
LABEL org.opencontainers.image.title="docker-bench" \
      org.opencontainers.image.description="Docker Bench for Security" \
      org.opencontainers.image.vendor="Docker" \
      org.opencontainers.image.source="https://github.com/docker/docker-bench-security" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
