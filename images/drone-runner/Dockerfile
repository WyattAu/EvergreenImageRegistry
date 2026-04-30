FROM debian:bookworm-slim AS downloader
ARG VERSION=1.0.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/harness/drone-runner-exec/releases/download/v${VERSION}/drone-runner-exec_linux_amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    tar -xzf /tmp/archive.tar.gz -C /tmp && \
    strip /tmp/drone-runner-exec && \
    chmod +x /tmp/drone-runner-exec

FROM scratch
COPY --from=downloader /tmp/drone-runner-exec /usr/local/bin/drone-runner-exec
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/usr/local/bin/drone-runner-exec"]
LABEL org.opencontainers.image.title="drone-runner" \
      org.opencontainers.image.description="Drone Runner Exec - shell command runner for Drone pipelines" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Harness" \
      org.opencontainers.image.source="https://github.com/harness/drone-runner-exec" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
