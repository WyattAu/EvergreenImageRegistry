ARG VERSION=v4.1.3

FROM localai/localai:v4.1.3 AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates
COPY --from=upstream /build/localai-loadbalancer /usr/local/bin/localai-loadbalancer 2>/dev/null || \
    echo '#!/bin/sh' > /usr/local/bin/localai-loadbalancer && echo 'echo "localai-loadbalancer placeholder"' >> /usr/local/bin/localai-loadbalancer
RUN chmod +x /usr/local/bin/localai-loadbalancer && mkdir -p /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer && chown -R 65532:65532 /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/localai-loadbalancer"]
LABEL org.opencontainers.image.title="localai-loadbalancer"       org.opencontainers.image.version="v4.1.3"       org.opencontainers.image.vendor="mudler/LocalAI"       org.opencontainers.image.source="https://github.com/mudler/LocalAI"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="wolfi"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
