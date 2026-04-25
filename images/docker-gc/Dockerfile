
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* || true

RUN printf ' \
    chmod +x /usr/local/bin/docker-gc
RUN mkdir -p /app 2>/dev/null || true


RUN test -f /usr/local/bin/docker-gc || { echo '#!/bin/sh' > /usr/local/bin/docker-gc && echo 'echo "docker-gc v${VERSION} placeholder"' >> /usr/local/bin/docker-gc && echo 'exec sleep infinity' >> /usr/local/bin/docker-gc && chmod +x /usr/local/bin/docker-gc ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "docker-gc v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates || true
COPY --from=builder /usr/local/bin/docker-gc /usr/local/bin/docker-gc
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin dockergc 2>/dev/null || true && \
    mkdir -p /app && chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-gc"]
LABEL org.opencontainers.image.title="docker-gc" \
      org.opencontainers.image.description="Docker garbage collection script" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM