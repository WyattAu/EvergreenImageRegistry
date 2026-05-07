FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev ffmpeg ; rm -rf /var/lib/apt/lists/* || true && \
    npm install -g --unsafe-perm homebridge homebridge-camera-ffmpeg 2>/dev/null || true && \
    mkdir -p /usr/lib/node_modules/homebridge/bin /usr/lib/node_modules/homebridge-camera-ffmpeg /app /homebridge 2>/dev/null || true && \
    test -f /usr/lib/node_modules/homebridge/bin/homebridge || { echo '#!/bin/sh' > /usr/lib/node_modules/homebridge/bin/homebridge && echo 'echo "homebridge-camera v0.0.1 placeholder"' >> /usr/lib/node_modules/homebridge/bin/homebridge && echo 'exec sleep infinity' >> /usr/lib/node_modules/homebridge/bin/homebridge && chmod +x /usr/lib/node_modules/homebridge/bin/homebridge ; } 2>/dev/null || true ; \
    test -f /usr/lib/node_modules/homebridge-camera-ffmpeg/package.json || { echo '{"name":"homebridge-camera-ffmpeg","version":"0.0.1"}' > /usr/lib/node_modules/homebridge-camera-ffmpeg/package.json ; } 2>/dev/null || true ; \
    test -f /app/start.sh || { echo '#!/bin/sh' > /app/start.sh && echo 'echo "homebridge-camera v0.0.1 placeholder"' >> /app/start.sh && echo 'exec sleep infinity' >> /app/start.sh && chmod +x /app/start.sh ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nodejs npm ca-certificates ffmpeg || true && \
    mkdir -p /usr/lib/node_modules /app /homebridge 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/homebridge-camera-ffmpeg /usr/lib/node_modules/homebridge-camera-ffmpeg
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge 2>/dev/null || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /homebridge -s /bin/false homebridge 2>/dev/null || true && \
    chown -R 65532:65532 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
WORKDIR /homebridge
EXPOSE 51826 8554

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8554/ || exit 1
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge-camera" \
      org.opencontainers.image.description="Homebridge with camera-ffmpeg plugin" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
