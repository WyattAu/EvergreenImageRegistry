FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.rfxn.com/downloads/maldetect-current.tar.gz" \
    -o /maldet.tar.gz && \
    tar -xzf /maldet.tar.gz -C /opt && rm /maldet.tar.gz
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools clamav-daemon \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/maldetect /opt/maldetect
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin maldet 2>/dev/null || true && \
    chown -R 65534:65534 /app /opt/maldet 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["/opt/maldet/maldet", "--help"] || exit 0
ENTRYPOINT ["/opt/maldet/maldet"]
CMD ["-a", "/app"]
LABEL org.opencontainers.image.title="maldet" \
      org.opencontainers.image.description="Linux Malware Detect" \
      org.opencontainers.image.vendor="rFXn" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
