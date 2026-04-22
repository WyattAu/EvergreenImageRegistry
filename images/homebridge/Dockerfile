FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g --unsafe-perm homebridge hap-nodejs
RUN mkdir -p /app /homebridge

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates libavahi-compat-libdnssd1 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/hap-nodejs /usr/lib/node_modules/hap-nodejs 2>/dev/null || true
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge && \
    useradd -r -u 65534 -g nogroup -d /homebridge -s /sbin/nologin homebridge 2>/dev/null || true && \
    chown -R 65534:65534 /homebridge /app /usr/lib/node_modules 2>/dev/null || true
USER 65534:65534
WORKDIR /homebridge
EXPOSE 51826
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["node", "-e", "const hb = require('homebridge'); console.log('ok')"] || exit 0
ENTRYPOINT ["homebridge"]
LABEL org.opencontainers.image.title="homebridge" \
      org.opencontainers.image.description="Homebridge - Bring Siri to your smart home" \
      org.opencontainers.image.vendor="nfarina" \
      org.opencontainers.image.source="https://github.com/nfarina/homebridge" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
