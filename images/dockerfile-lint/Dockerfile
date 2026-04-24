
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*RUN npm install -g dockerfilelint
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /usr/lib/node_modules/dockerfilelint /app/dockerfilelint
COPY --from=builder /usr/bin/dockerfilelint /usr/local/bin/dockerfilelint
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin dockerlint 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["dockerfilelint"]
LABEL org.opencontainers.image.title="dockerfile-lint" \
      org.opencontainers.image.description="Dockerfile linter" \
      org.opencontainers.image.vendor="replicated" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM