
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        cockpit cockpit-ws cockpit-dashboard cockpit-storaged cockpit-system ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin cockpit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["cockpit-ws"]
CMD ["--port", "9090"]
LABEL org.opencontainers.image.title="cockpit" \
      org.opencontainers.image.description="Cockpit - Web-based server management" \
      org.opencontainers.image.vendor="Red Hat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM