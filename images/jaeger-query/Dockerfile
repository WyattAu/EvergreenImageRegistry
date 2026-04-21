# =============================================================================
# SOVEREIGN HARDENED JAEGER-QUERY
# Generated from template - Version: 1.55.0
# Distributed tracing query service
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.55.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/jaegertracing/jaeger/releases/download/v1.55.0/jaeger-1.55.0-linux-amd64.tar.gz" -o /jaeger.tar.gz && \
    tar -xzf /jaeger.tar.gz -C /tmp && rm /jaeger.tar.gz && \
    strip --strip-all /tmp/jaeger-1.55.0-linux-amd64/jaeger-query && \
    mv /tmp/jaeger-1.55.0-linux-amd64/jaeger-query /jaeger-query

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jaeger

FROM scratch
COPY --from=downloader /jaeger-query /jaeger-query
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/jaeger /var/log/jaeger
USER 65534:65534
WORKDIR /app
EXPOSE 16686
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/jaeger-query", "--version"]
ENTRYPOINT ["/jaeger-query"]
LABEL org.opencontainers.image.title="jaeger-query" \
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
