FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.rfxn.com/downloads/maldetect-current.tar.gz" \
    -o /maldet.tar.gz && \
    tar -xzf /maldet.tar.gz -C /opt && rm /maldet.tar.gz
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates inotify-tools clamav-daemon
COPY --from=builder /opt/maldetect /opt/maldetect
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin maldet 2>/dev/null || true && \
    chown -R 65532:65532 /app /opt/maldet 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/opt/maldet/maldet"]
CMD ["-a", "/app"]
LABEL org.opencontainers.image.title="maldet" \
      org.opencontainers.image.description="Linux Malware Detect" \
      org.opencontainers.image.vendor="rFXn" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM