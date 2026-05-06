ARG VERSION=2.12.0

FROM ghcr.io/opensearch-project/opensearch-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/opensearch-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/opensearch-operator"]
LABEL org.opencontainers.image.title="opensearch-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.description="OpenSearch Operator for Kubernetes" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="go" \
      evergreen.hft.runtime-hints="GOMAXPROCS=<cores>" \
            org.opencontainers.image.source="https://github.com/opensearch-project/opensearch-k8s-operator"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
