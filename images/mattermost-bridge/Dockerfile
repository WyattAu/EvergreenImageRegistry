FROM debian:bookworm-slim AS downloader
ARG VERSION=1.2.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mattermost/mattermost-plugin-github/releases/download/v${VERSION}/github-linux-amd64.tar.gz" \
    -o /tmp/archive.tar.gz && \
    mkdir -p /tmp/plugin && \
    tar -xzf /tmp/archive.tar.gz -C /tmp/plugin && \
    find /tmp/plugin -type f -executable -exec strip {} \; 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.2.0
RUN apk add --no-cache ca-certificates || true
RUN addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true
COPY --from=downloader /tmp/plugin /app/plugin
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8065
ENTRYPOINT ["/app/plugin/server"]
LABEL org.opencontainers.image.title="mattermost-bridge" \
      org.opencontainers.image.description="Mattermost GitHub Plugin - GitHub integration bridge for Mattermost" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost-plugin-github" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
