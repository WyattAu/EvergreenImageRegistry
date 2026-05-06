FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=6.4.6
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mattermost/mattermost-push-proxy/releases/download/v${VERSION}/mattermost-push-proxy-linux-amd64" \
    -o /tmp/binary && \
    strip /tmp/binary && \
    chmod +x /tmp/binary
FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/mattermost-push-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8066

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/mattermost-push-proxy"]
LABEL org.opencontainers.image.title="mattermost-push-proxy" \
      org.opencontainers.image.description="Mattermost Push Proxy - push notification proxy for Mattermost mobile apps" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost-push-proxy" \
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
