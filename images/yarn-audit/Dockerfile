FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g yarn
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /usr/bin/yarn /usr/local/bin/yarn 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin yarnaudit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["yarn", "--version"]
ENTRYPOINT ["yarn"]
CMD ["audit"]
LABEL org.opencontainers.image.title="yarn-audit" \
      org.opencontainers.image.description="Yarn audit wrapper" \
      org.opencontainers.image.vendor="Yarn" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
