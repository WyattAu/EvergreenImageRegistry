
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g iobroker
RUN mkdir -p /app /opt/iobroker 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs npm ca-certificates 
COPY --from=builder /opt/iobroker /opt/iobroker
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /opt/iobroker -s /bin/false iobroker 2>/dev/null || true && \
    chown -R 65532:65532 /opt/iobroker /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/iobroker
EXPOSE 8081 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3000/ || exit 1
ENTRYPOINT ["iobroker"]
CMD ["start"]
LABEL org.opencontainers.image.title="iobroker" \
      org.opencontainers.image.description="ioBroker - IoT automation platform" \
      org.opencontainers.image.vendor="ioBroker" \
      org.opencontainers.image.source="https://github.com/ioBroker/ioBroker" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
