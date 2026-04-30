FROM debian:bookworm-slim AS downloader
ARG VERSION=2.7.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/woodpecker-ci/woodpecker/releases/download/v${VERSION}/woodpecker-agent_linux_amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/woodpecker-agent && \
    chmod +x /tmp/woodpecker-agent

FROM scratch
COPY --from=downloader /tmp/woodpecker-agent /usr/local/bin/woodpecker-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/usr/local/bin/woodpecker-agent"]
LABEL org.opencontainers.image.title="woodpecker-agent" \
      org.opencontainers.image.description="Woodpecker Agent - CI/CD build agent for Woodpecker CI" \
      org.opencontainers.image.version="2.7.0" \
      org.opencontainers.image.vendor="Woodpecker CI" \
      org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
