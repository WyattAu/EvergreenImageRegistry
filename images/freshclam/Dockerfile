FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav-freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/lib/clamav /var/log/clamav

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav-freshclam ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/lib/clamav /var/lib/clamav
COPY --from=builder /var/log/clamav /var/log/clamav
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin freshclam 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/lib/clamav /var/log/clamav 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=1 \
    CMD ["freshclam", "--version"]
ENTRYPOINT ["freshclam"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="freshclam" \
      org.opencontainers.image.description="FreshClam - ClamAV database updater" \
      org.opencontainers.image.vendor="Cisco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
