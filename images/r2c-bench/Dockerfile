
FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 ca-certificates || true
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin r2c 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="r2c-bench" \
      org.opencontainers.image.description="Placeholder - r2c benchmark" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM