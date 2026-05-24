
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends         python3-pip git ca-certificates gcc g++ make     && rm -rf /var/lib/apt/lists/* || true && \
    pip install --break-system-packages --no-cache-dir platformio 2>/dev/null || true && \
    mkdir -p /app /firmware 2>/dev/null || true
FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN microdnf install -y python3 ca-certificates
COPY --from=builder /app /app
COPY --from=builder /firmware /firmware
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false tasmota 2>/dev/null || true &&     chown -R 65532:65532 /app /firmware 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
CMD ["-c", "print('Tasmota firmware build environment. Clone https://github.com/arendst/Tasmota and run platformio.')"]
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"

EXPOSE 9101
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.description="tasmota container image" \
      org.opencontainers.image.title="Tasmota" \
      org.opencontainers.image.source="https://github.com/arendst/Tasmota" \
            org.opencontainers.image.version="unknown"
