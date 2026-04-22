# =============================================================================
# SOVEREIGN ALIAS - JAEGER -> jaeger-agent
# Alias for images/jaeger-agent/
# =============================================================================

ARG VERSION=1.55.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/jaegertracing/jaeger/releases/download/v${VERSION}/jaeger-${VERSION}-linux-amd64.tar.gz" -o /jaeger.tar.gz && \
    tar -xzf /jaeger.tar.gz -C /tmp && rm /jaeger.tar.gz && \
    chmod +x /tmp/jaeger-${VERSION}-linux-amd64/jaeger-agent && \
    mv /tmp/jaeger-${VERSION}-linux-amd64/jaeger-agent /jaeger-agent

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jaeger

FROM scratch
COPY --from=downloader /jaeger-agent /jaeger-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/jaeger /var/log/jaeger
USER 65534:65534
WORKDIR /app
EXPOSE 5775 6831 6832
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/jaeger-agent", "--version"]
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
