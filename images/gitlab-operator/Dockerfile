ARG VERSION=0.8.0

FROM registry.gitlab.com/gitlab-org/cloud-native/gitlab-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/gitlab-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/gitlab-operator"]
LABEL org.opencontainers.image.title="gitlab-operator" \
      org.opencontainers.image.description="GitLab Operator - Kubernetes operator for GitLab" \
      org.opencontainers.image.version="${VERSION}" \
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
