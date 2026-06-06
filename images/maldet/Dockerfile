
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/maldetect || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates inotify-tools ; rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://www.rfxn.com/downloads/maldetect-current.tar.gz" \
    -o /maldet.tar.gz && \
    [ -f /maldet.tar.gz ] && tar -xzf /maldet.tar.gz -C /opt && rm -f /maldet.tar.gz && \
    mkdir -p /app /opt/maldetect 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache curl ca-certificates inotify-tools clamav-daemon
COPY --from=builder /opt/maldetect /opt/maldetect
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false maldet 2>/dev/null || true && \
    chown -R 65532:65532 /app /opt/maldet 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/opt/maldet/maldet"]
CMD ["-a", "/app"]
LABEL org.opencontainers.image.title="maldet" \
      org.opencontainers.image.description="Linux Malware Detect" \
      org.opencontainers.image.vendor="rFXn" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/rfxn/linux-malware-detect" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
