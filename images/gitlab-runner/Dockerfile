ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG TARGETARCH
ARG VERSION=16.11.0

RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://gitlab-runner-downloads.s3.amazonaws.com/v${VERSION}/binaries/gitlab-runner-linux-${TARGETARCH}" -o /tmp/gitlab-runner && \
    echo "c903479cefb95db6a29b24394a05cec9101688500c2e4e221b061259de321a79  /tmp/gitlab-runner" | sha256sum -c ; \
    chmod +x /tmp/gitlab-runner && strip /tmp/gitlab-runner && \
    test -f /tmp/gitlab-runner

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim
RUN chmod +x /shim
COPY --from=downloader /tmp/gitlab-runner /usr/local/bin/gitlab-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8093
LABEL org.opencontainers.image.title="gitlab-runner" \
      org.opencontainers.image.description="GitLab Runner - CI/CD runner for GitLab" \
      org.opencontainers.image.version="16.11.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-runner" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8093"]

ENTRYPOINT ["/shim", "run"]
