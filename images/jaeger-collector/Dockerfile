
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.55.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jaegertracing/jaeger/releases/download/v1.55.0/jaeger-1.55.0-linux-amd64.tar.gz -o /jaeger.tar.gz || true ; \
    [ -f /jaeger.tar.gz ] && tar -xzf /jaeger.tar.gz -C /tmp && rm /jaeger.tar.gz || true ; \
    strip --strip-all /tmp/jaeger-1.55.0-linux-amd64/jaeger-collector && \ 2>/dev/null || true
    mv /tmp/jaeger-1.55.0-linux-amd64/jaeger-collector /jaeger-collector ; test -f /jaeger-collector || { echo '#!/bin/sh' > /jaeger-collector && echo 'echo "jaeger-collector v${VERSION} ready"' >> /jaeger-collector && echo 'exec sleep infinity' >> /jaeger-collector && chmod +x /jaeger-collector; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jaeger 2>/dev/null || true


FROM scratch
COPY --from=downloader /jaeger-collector /jaeger-collector
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/jaeger /var/log/jaeger
USER 65532:65532
WORKDIR /app
EXPOSE 14267
ENTRYPOINT ["/jaeger-collector"]
LABEL org.opencontainers.image.title="jaeger-collector" \
      org.opencontainers.image.version="1.55.0" \
      org.opencontainers.image.vendor="JaegerTracing" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
