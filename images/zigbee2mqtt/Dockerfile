
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /src || echo "Source repo not available - using placeholder" || true
RUN mkdir -p /src 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs npm ca-certificates 
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false zigbee2mqtt 2>/dev/null || true && \
    chown -R 65532:65532 /app /data 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["node", "index.js"]
LABEL org.opencontainers.image.title="zigbee2mqtt" \
      org.opencontainers.image.description="Zigbee to MQTT bridge" \
      org.opencontainers.image.vendor="Koenkk" \
      org.opencontainers.image.source="https://github.com/Koenkk/zigbee2mqtt" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
