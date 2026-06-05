ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.7.1
ARG TARGETARCH
RUN mkdir -p /tmp/plugin || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/mattermost/mattermost-plugin-github/releases/download/v${VERSION}/mattermost-plugin-github-v${VERSION}-linux-amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    echo "a7877284ec2e00c8c3a27dad11077aeb1dece647882ea69fa18f651d010cc266  /tmp/archive.tar.gz" | sha256sum -c && \
    mkdir -p /tmp/plugin && \
    tar -xzf /tmp/archive.tar.gz -C /tmp/plugin && \
    find /tmp/plugin -type f -executable -exec strip {} \; 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.7.1
RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 10000 appuser 2>/dev/null  && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true
COPY --from=downloader /tmp/plugin /app/plugin
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8065

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8065"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="mattermost-bridge" \
      org.opencontainers.image.description="Mattermost GitHub Plugin - GitHub integration bridge for Mattermost" \
      org.opencontainers.image.version="2.7.1" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost-plugin-github" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
