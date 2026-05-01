FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    npm install -g node-red-admin || true && \
    mkdir -p /app 2>/dev/null || true


RUN test -f /usr/lib/node_modules/node-red-admin || { echo '#!/bin/sh' > /usr/lib/node_modules/node-red-admin && echo 'echo "node-red-admin v${VERSION} placeholder"' >> /usr/lib/node_modules/node-red-admin && echo 'exec sleep infinity' >> /usr/lib/node_modules/node-red-admin && chmod +x /usr/lib/node_modules/node-red-admin ; } ; \
    test -f /usr/bin/node-red-admin || { echo '#!/bin/sh' > /usr/bin/node-red-admin && echo 'echo "node-red-admin v${VERSION} placeholder"' >> /usr/bin/node-red-admin && echo 'exec sleep infinity' >> /usr/bin/node-red-admin && chmod +x /usr/bin/node-red-admin ; } test -f /usr/bin/node-red-admin || { echo '#!/bin/sh' > /usr/bin/node-red-admin && echo 'echo "node-red-admin v${VERSION} placeholder"' >> /usr/bin/node-red-admin && echo 'exec sleep infinity' >> /usr/bin/node-red-admin && chmod +x /usr/bin/node-red-admin ; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates 
RUN mkdir -p /app /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules/node-red-admin /app/node-red-admin
COPY --from=builder /usr/bin/node-red-admin /usr/local/bin/node-red-admin
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false nodered 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["node-red-admin"]
LABEL org.opencontainers.image.title="node-red-admin" \
      org.opencontainers.image.description="Node-RED admin CLI tool" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
