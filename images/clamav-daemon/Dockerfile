
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/clamav /var/lib/clamav /run/clamav


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache clamav clamav-daemon freshclam ca-certificates
COPY --from=builder /app /app
COPY --from=builder /var/log/clamav /var/log/clamav
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /run/clamav /run/clamav
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin clamav 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/clamav /var/lib/clamav /run/clamav 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["clamd"]
CMD ["--foreground", "--debug"]
LABEL org.opencontainers.image.title="clamav-daemon" \
      org.opencontainers.image.description="ClamAV - daemon mode" \
      org.opencontainers.image.vendor="Cisco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM