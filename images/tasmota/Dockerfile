
ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends         python3-pip git ca-certificates gcc g++ make     && rm -rf /var/lib/apt/lists/* || true && \
    pip install --break-system-packages --no-cache-dir platformio 2>/dev/null || true && \
    mkdir -p /app /firmware 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache python3 ca-certificates 
COPY --from=builder /app /app
COPY --from=builder /firmware /firmware
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false tasmota 2>/dev/null || true &&     chown -R 65532:65532 /app /firmware 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
CMD ["-c", "print('Tasmota firmware build environment. Clone https://github.com/arendst/Tasmota and run platformio.')"]
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.description="tasmota container image" \
      org.opencontainers.image.source="https://github.com/arendst/Tasmota" \
            org.opencontainers.image.version="unknown"
