FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/clamav /var/lib/clamav /run/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/clamav /var/log/clamav
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /run/clamav /run/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin clamav 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/clamav /var/lib/clamav /run/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD ["clamscan", "--version"]
ENTRYPOINT ["clamd"]
CMD ["--foreground", "--debug"]
LABEL org.opencontainers.image.title="clamav-daemon" \
      org.opencontainers.image.description="ClamAV - daemon mode" \
      org.opencontainers.image.vendor="Cisco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
