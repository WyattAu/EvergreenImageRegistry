FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin transfer 2>/dev/null || true && \
    mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["echo", "ok"]
ENTRYPOINT ["echo"]
CMD ["transferhelper: transfer file helper utility"]
LABEL org.opencontainers.image.title="transferhelper" \
      org.opencontainers.image.description="Placeholder - Transfer helper utility" \
      sovereign.image.tier="3" \
      sovereign.image.status="placeholder" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
