FROM debian:bookworm-slim AS downloader
ARG VERSION=1.1.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
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
ENTRYPOINT ["/usr/local/bin/mattermost-push-proxy"]
LABEL org.opencontainers.image.title="mattermost-push-proxy" \
      org.opencontainers.image.description="Mattermost Push Proxy - push notification proxy for Mattermost mobile apps" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost-push-proxy" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
