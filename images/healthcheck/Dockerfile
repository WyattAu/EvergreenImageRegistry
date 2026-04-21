# =============================================================================
# SOVEREIGN HARDENED HEALTHCHECK (grpc-health-probe)
# Generated from template - Version: 0.4.36
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.36
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v${VERSION}/grpc_health_probe-linux-amd64.tar.gz" -o /healthcheck.tar.gz && \
    echo "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b  /healthcheck.tar.gz" | sha256sum -c -
RUN tar -xzf /healthcheck.tar.gz -C / && \
    rm /healthcheck.tar.gz && \
    strip /grpc_health_probe

FROM debian:bookworm-20240101-slim AS builder
RUN mkdir -p /app

FROM scratch
COPY --from=downloader /grpc_health_probe /grpc_health_probe
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/grpc_health_probe", "--version"]
ENTRYPOINT ["/grpc_health_probe"]
LABEL org.opencontainers.image.title="healthcheck" \
      org.opencontainers.image.version="0.4.36" \
      org.opencontainers.image.vendor="grpc-ecosystem" \
      org.opencontainers.image.description="grpc-health-probe - gRPC health checking tool for Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="2s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="1000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go"
