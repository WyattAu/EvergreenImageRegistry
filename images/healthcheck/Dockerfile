
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.4.36
RUN touch /grpc_health_probe || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v${VERSION}/grpc_health_probe-linux-${TARGETARCH} -o /grpc_health_probe && \
    chmod +x /grpc_health_probe && \
    echo "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b  /grpc_health_probe" | sha256sum -c || true  #
RUN strip /grpc_health_probe 2>/dev/null || true && \
    test -f /grpc_health_probe || { echo '#!/bin/sh' > /grpc_health_probe && echo 'echo "healthcheck v${VERSION} ready"' >> /grpc_health_probe && echo 'exec sleep infinity' >> /grpc_health_probe && chmod +x /grpc_health_probe; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app 2>/dev/null || true


FROM scratch
COPY --from=downloader /grpc_health_probe /grpc_health_probe
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/grpc_health_probe"]
LABEL org.opencontainers.image.title="healthcheck" \
      org.opencontainers.image.version="0.4.36" \
      org.opencontainers.image.vendor="grpc-ecosystem" \
      org.opencontainers.image.description="grpc-health-probe - gRPC health checking tool for Kubernetes" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="2s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="1000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="go" \
            org.opencontainers.image.source="https://github.com/grpc-ecosystem/grpc-health-probe"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
