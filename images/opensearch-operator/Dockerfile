# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH-OPERATOR
# Generated from template - Version: 2.9.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.9.0
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/opensearch-project/opensearch-operator/releases/download/v${VERSION}/opensearch-operator_linux_amd64" -o /opensearch-operator && \
    echo "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4  /opensearch-operator" | sha256sum -c - && \
    chmod +x /opensearch-operator && \
    strip /opensearch-operator

FROM debian:bookworm-20240101-slim AS builder
RUN mkdir -p /app /var/log/opensearch-operator

FROM scratch
COPY --from=downloader /opensearch-operator /opensearch-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/opensearch-operator /var/log/opensearch-operator
USER 65534:65534
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opensearch-operator", "--version"]
ENTRYPOINT ["/opensearch-operator"]
LABEL org.opencontainers.image.title="opensearch-operator" \
      org.opencontainers.image.version="2.9.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.description="OpenSearch Operator for Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go" \
      sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"
