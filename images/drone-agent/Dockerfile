FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.24.1
ARG TARGETARCH
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/harness/drone/releases/download/v${VERSION}/drone_agent_linux_amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/drone-agent  || true&& \
    chmod +x /tmp/drone-agent
FROM scratch
COPY --from=downloader /tmp/drone-agent /usr/local/bin/drone-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/drone-agent"]
LABEL org.opencontainers.image.title="drone-agent" \
      org.opencontainers.image.description="Drone Agent - CI/CD build agent for Drone" \
      org.opencontainers.image.version="2.24.1" \
      org.opencontainers.image.vendor="Harness" \
      org.opencontainers.image.source="https://github.com/harness/drone" \
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
