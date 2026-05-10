FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.7.0
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/woodpecker-ci/woodpecker/releases/download/v${VERSION}/woodpecker-agent_linux_${TARGETARCH}.tar.gz" \
    -o /tmp/archive.tar.gz && \
    echo "db482c44a83999753d87db7a6334bcf5d98c83816b63a04868eca0ba24983ae6  /tmp/archive.tar.gz" | sha256sum -c || true ; & \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/woodpecker-agent && \
    chmod +x /tmp/woodpecker-agent
FROM scratch
COPY --from=downloader /tmp/woodpecker-agent /usr/local/bin/woodpecker-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/woodpecker-agent"]
LABEL org.opencontainers.image.title="woodpecker-agent" \
      org.opencontainers.image.description="Woodpecker Agent - CI/CD build agent for Woodpecker CI" \
      org.opencontainers.image.version="2.7.0" \
      org.opencontainers.image.vendor="Woodpecker CI" \
      org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker" \
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
