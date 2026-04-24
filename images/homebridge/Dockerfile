
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev \
    && rm -rf /var/lib/apt/lists/*RUN npm install -g --unsafe-perm homebridge hap-nodejs
RUN mkdir -p /app /homebridge


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/hap-nodejs /usr/lib/node_modules/hap-nodejs 2>/dev/null || true
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge && \
    adduser -u 65532 -G nogroup -D -h /homebridge -s /sbin/nologin homebridge 2>/dev/null || true && \
    chown -R 65532:65532 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
WORKDIR /homebridge
EXPOSE 51826
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge" \
      org.opencontainers.image.description="Homebridge - Bring Siri to your smart home" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM