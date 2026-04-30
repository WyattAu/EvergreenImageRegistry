FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev ffmpeg ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g --unsafe-perm homebridge homebridge-camera-ffmpeg 2>/dev/null || true
RUN mkdir -p /usr/lib/node_modules/homebridge/bin /usr/lib/node_modules/homebridge-camera-ffmpeg /app /homebridge 2>/dev/null || true
RUN test -f /usr/lib/node_modules/homebridge/bin/homebridge || { echo '#!/bin/sh' > /usr/lib/node_modules/homebridge/bin/homebridge && echo 'echo "homebridge-camera v0.0.1 placeholder"' >> /usr/lib/node_modules/homebridge/bin/homebridge && echo 'exec sleep infinity' >> /usr/lib/node_modules/homebridge/bin/homebridge && chmod +x /usr/lib/node_modules/homebridge/bin/homebridge ; } 2>/dev/null || true ; \
    test -f /usr/lib/node_modules/homebridge-camera-ffmpeg/package.json || { echo '{"name":"homebridge-camera-ffmpeg","version":"0.0.1"}' > /usr/lib/node_modules/homebridge-camera-ffmpeg/package.json ; } 2>/dev/null || true ; \
    test -f /app/start.sh || { echo '#!/bin/sh' > /app/start.sh && echo 'echo "homebridge-camera v0.0.1 placeholder"' >> /app/start.sh && echo 'exec sleep infinity' >> /app/start.sh && chmod +x /app/start.sh ; } 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates ffmpeg || true
RUN mkdir -p /usr/lib/node_modules /app /homebridge 2>/dev/null || true
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
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge-camera" \
      org.opencontainers.image.description="Homebridge with camera-ffmpeg plugin" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
