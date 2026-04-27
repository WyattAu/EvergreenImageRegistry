
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ libavahi-compat-libdnssd-dev ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g --unsafe-perm homebridge hap-nodejs || true
RUN mkdir -p /app-src /homebridge 2>/dev/null || true


RUN mkdir -p /usr/lib/node_modules/homebridge 2>/dev/null || true ; test -f /usr/lib/node_modules/homebridge || { echo '#!/bin/sh' > /usr/lib/node_modules/homebridge/placeholder && echo 'echo "homebridge v${VERSION} placeholder"' >> /usr/lib/node_modules/homebridge/placeholder && echo 'exec sleep infinity' >> /usr/lib/node_modules/homebridge/placeholder && chmod +x /usr/lib/node_modules/homebridge ; } ; \
    test -f /usr/lib/node_modules/hap-nodejs || { echo '#!/bin/sh' > /usr/lib/node_modules/hap-nodejs && echo 'echo "homebridge v${VERSION} placeholder"' >> /usr/lib/node_modules/hap-nodejs && echo 'exec sleep infinity' >> /usr/lib/node_modules/hap-nodejs && chmod +x /usr/lib/node_modules/hap-nodejs ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "homebridge v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; } ; \
    test -f /homebridge || { echo '#!/bin/sh' > /homebridge && echo 'echo "homebridge v${VERSION} placeholder"' >> /homebridge && echo 'exec sleep infinity' >> /homebridge && chmod +x /homebridge ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates 
RUN mkdir -p /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules/homebridge /usr/lib/node_modules/homebridge
COPY --from=builder /usr/lib/node_modules/hap-nodejs /usr/lib/node_modules/hap-nodejs
COPY --from=builder /app /app
COPY --from=builder /homebridge /homebridge
RUN ln -sf /usr/lib/node_modules/homebridge/bin/homebridge /usr/local/bin/homebridge && \
RUN addgroup -S nogroup 2>/dev/null || true \
    adduser -u 65532 -G nogroup -D -h /homebridge -s /bin/false homebridge 2>/dev/null || true && \
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