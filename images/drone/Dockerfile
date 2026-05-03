# =============================================================================
# EVERGREEN HARDENED DRONE
# Generated from template - Version: 2.28.1
# Downloads Drone binary directly from GitHub releases (no upstream image).
# Drone is a Go static binary.
# =============================================================================

ARG VERSION=2.28.1
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.28.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/harness/drone/releases/download/v${VERSION}/drone_linux_amd64.tar.gz" -o /tmp/drone.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/drone.tar.gz -C /app && rm -f /tmp/drone.tar.gz && \
    strip --strip-all /app/drone && \
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
      org.opencontainers.image.version="2.28.1" \
      org.opencontainers.image.vendor="Drone" \
      org.opencontainers.image.source="https://github.com/drone/drone" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
