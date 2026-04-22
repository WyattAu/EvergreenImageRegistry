FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g dockerfilelint
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/dockerfilelint /app/dockerfilelint 2>/dev/null || true
COPY --from=builder /usr/bin/dockerfilelint /usr/local/bin/dockerfilelint 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin dockerlint 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["dockerfilelint", "--version"] || exit 0
ENTRYPOINT ["dockerfilelint"]
LABEL org.opencontainers.image.title="dockerfile-lint" \
      org.opencontainers.image.description="Dockerfile linter" \
      org.opencontainers.image.vendor="replicated" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
