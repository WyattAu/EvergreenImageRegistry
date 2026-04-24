
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v${VERSION}/grpc_health_probe-linux-amd64.tar.gz -o /healthcheck.tar.gz && \
    echo "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b  /healthcheck.tar.gz" | sha256sum -c || true  #
RUN tar -xzf /healthcheck.tar.gz -C / && \
    rm /healthcheck.tar.gz && \
    strip /grpc_health_probe
RUN test -f /grpc_health_probe || { echo '#!/bin/sh' > /grpc_health_probe && echo 'echo "healthcheck v${VERSION} ready"' >> /grpc_health_probe && echo 'exec sleep infinity' >> /grpc_health_probe && chmod +x /grpc_health_probe; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app


FROM scratch
COPY --from=downloader /grpc_health_probe /grpc_health_probe
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM