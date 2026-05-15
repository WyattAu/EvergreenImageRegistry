# =============================================================================
# EVERGREEN HARDENED DRONE
# Generated from template - Version: 1.9.0
# Downloads Drone CLI binary from harness/drone-cli releases.
# Drone is a Go static binary.
# =============================================================================

ARG VERSION=1.9.0
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.9.0
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN mkdir -p /app
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/harness/drone-cli/releases/download/v${VERSION}/drone_linux_${TARGETARCH}.tar.gz" -o /tmp/drone.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/drone.tar.gz -C /app && rm -f /tmp/drone.tar.gz && \
    strip --strip-all /app/drone  || true 2>/dev/null && \
    chmod +x /app/drone
FROM scratch
COPY --from=downloader /app/drone /drone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /data

HEALTHCHECK NONE
ENTRYPOINT ["/drone"]
EXPOSE 80

LABEL org.opencontainers.image.title="drone" \
      org.opencontainers.image.description="Drone - cloud-native continuous integration and delivery platform" \
       org.opencontainers.image.version="1.9.0" \
       org.opencontainers.image.vendor="Harness" \
       org.opencontainers.image.source="https://github.com/harness/drone-cli" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
