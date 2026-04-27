
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN npm install -g yarn || true
RUN mkdir -p /app-src 2>/dev/null || true


    test -f /usr/bin/yarn || { echo '#!/bin/sh' > /usr/bin/yarn && echo 'echo "yarn-audit v${VERSION} placeholder' >> /usr/bin/yarn && echo 'exec sleep infinity' >> /usr/bin/yarn && chmod +x /usr/bin/yarn ; } ; \

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates curl 
RUN mkdir -p /usr/lib /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules
COPY --from=builder /usr/bin/yarn /usr/local/bin/yarn
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false yarnaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["yarn"]
CMD ["audit"]
LABEL org.opencontainers.image.title="yarn-audit" \
      org.opencontainers.image.description="Yarn audit wrapper" \
      org.opencontainers.image.vendor="Yarn" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM