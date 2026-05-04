FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.2.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mattermost/mattermost-plugin-github/releases/download/v${VERSION}/github-linux-amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    mkdir -p /tmp/plugin && \
    tar -xzf /tmp/archive.tar.gz -C /tmp/plugin && \
    find /tmp/plugin -type f -executable -exec strip {} \; 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=1.2.0
RUN apk add --no-cache ca-certificates || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true
COPY --from=downloader /tmp/plugin /app/plugin
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8065

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8065/ || exit 1
ENTRYPOINT ["/app/plugin/server"]
LABEL org.opencontainers.image.title="mattermost-bridge" \
      org.opencontainers.image.description="Mattermost GitHub Plugin - GitHub integration bridge for Mattermost" \
      org.opencontainers.image.version="1.2.0" \
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
