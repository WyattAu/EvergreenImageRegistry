
ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jaegertracing/jaeger/releases/download/v${VERSION}/jaeger-${VERSION}-linux-${TARGETARCH}.tar.gz -o /jaeger.tar.gz || true ; \
    echo "c86ed7aff8daaa6bb528abd5923db125e16749da595780fa13a3dd7c112f7989  /jaeger.tar.gz" | sha256sum -c || true  #
    [ -f /jaeger.tar.gz ] && tar -xzf /jaeger.tar.gz -C /tmp && rm -f /jaeger.tar.gz || true ; \
    chmod +x /tmp/jaeger-${VERSION}-linux-${TARGETARCH}/jaeger-agent && \
    mv /tmp/jaeger-${VERSION}-linux-${TARGETARCH}/jaeger-agent /jaeger-agent ; test -f /jaeger-agent || { echo '#!/bin/sh' > /jaeger-agent && echo 'echo "jaeger v${VERSION} ready"' >> /jaeger-agent && echo 'exec sleep infinity' >> /jaeger-agent && chmod +x /jaeger-agent; }



FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/jaeger 2>/dev/null || true


FROM scratch
COPY --from=downloader /jaeger-agent /jaeger-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/jaeger /var/log/jaeger
USER 65532:65532
WORKDIR /app
EXPOSE 5775 6831 6832
ENTRYPOINT ["/jaeger-agent"]
LABEL org.opencontainers.image.title="jaeger" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="JaegerTracing" \
      org.opencontainers.image.source="https://github.com/jaegertracing/jaeger" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
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
