FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/clamav /var/lib/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/clamav /var/log/clamav
COPY --from=builder /var/lib/clamav /var/lib/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin clamav 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/clamav /var/lib/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD ["clamscan", "--version"]
ENTRYPOINT ["clamd"]
CMD ["--foreground"]
LABEL org.opencontainers.image.title="clamav" \
      org.opencontainers.image.description="ClamAV - open source antivirus engine" \
      org.opencontainers.image.vendor="Cisco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
