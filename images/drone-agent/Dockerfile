FROM debian:bookworm-slim AS downloader
ARG VERSION=2.24.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/harness/drone/releases/download/v${VERSION}/drone_agent_linux_amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/drone-agent && \
    chmod +x /tmp/drone-agent

FROM scratch
COPY --from=downloader /tmp/drone-agent /usr/local/bin/drone-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/usr/local/bin/drone-agent"]
LABEL org.opencontainers.image.title="drone-agent" \
      org.opencontainers.image.description="Drone Agent - CI/CD build agent for Drone" \
      org.opencontainers.image.version="2.24.1" \
      org.opencontainers.image.vendor="Harness" \
      org.opencontainers.image.source="https://github.com/harness/drone" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
