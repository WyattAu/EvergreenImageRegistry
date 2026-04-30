FROM debian:bookworm-slim AS downloader
ARG VERSION=0.8.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://gitlab.com/api/v4/projects/gitlab-org%2Fcloud-native%2Fgitlab-operator/packages/generic/gitlab-operator/${VERSION}/gitlab-operator-linux-amd64" -o /tmp/gitlab-operator && \
    chmod +x /tmp/gitlab-operator && strip /tmp/gitlab-operator || true
RUN test -f /tmp/gitlab-operator && test -s /tmp/gitlab-operator || { echo "ERROR: gitlab-operator binary not downloaded" >&2; exit 1; }

FROM scratch
COPY --from=downloader /tmp/gitlab-operator /usr/local/bin/gitlab-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="gitlab-operator" \
      org.opencontainers.image.description="GitLab Operator - Kubernetes operator for GitLab" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/cloud-native/gitlab-operator" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["gitlab-operator"]
