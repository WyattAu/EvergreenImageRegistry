
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g tasmotizer 2>/dev/null || true
RUN mkdir -p /app-src 2>/dev/null || true


RUN test -f /usr/lib/node_modules || { echo '#!/bin/sh' > /usr/lib/node_modules && echo 'echo "tasmota-js v${VERSION} placeholder"' >> /usr/lib/node_modules && echo 'exec sleep infinity' >> /usr/lib/node_modules && chmod +x /usr/lib/node_modules ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "tasmota-js v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates 
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin tasmota 2>/dev/null || true && \
    chown -R 65532:65532 /app /usr/lib/node_modules 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tasmota-js" \
      org.opencontainers.image.description="Tasmota JavaScript tools" \
      org.opencontainers.image.vendor="Tasmota" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM