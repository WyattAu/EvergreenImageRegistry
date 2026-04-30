FROM debian:bookworm-slim AS downloader
ARG VERSION=1.12.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mattermost/mattermost-operator/releases/download/v${VERSION}/mattermost-kubernetes-operator-linux-amd64" \
    -o /tmp/binary && \
    strip /tmp/binary && \
    chmod +x /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/mattermost-kubernetes-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/mattermost-kubernetes-operator"]
LABEL org.opencontainers.image.title="mattermost-operator" \
      org.opencontainers.image.description="Mattermost Kubernetes Operator - manages Mattermost deployments on Kubernetes" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost-operator" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
