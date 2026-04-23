# =============================================================================
# SOVEREIGN HARDENED DRONE-AUTOSCALER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.28.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/harness/drone/releases/download/v2.28.1/drone_linux_amd64.tar.gz" -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/drone-autoscaler /tmp/drone-autoscaler_stripped &&     strip /tmp/drone-autoscaler_stripped &&     chmod +x /tmp/drone-autoscaler_stripped

FROM scratch
COPY --from=downloader /tmp/drone-autoscaler_stripped /usr/local/bin/drone-autoscaler
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="drone-autoscaler"       org.opencontainers.image.description="Drone Autoscaler - automatic scaling for Drone runners"       org.opencontainers.image.version="2.28.1"       org.opencontainers.image.vendor="Harness"       org.opencontainers.image.source="https://github.com/harness/drone"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM