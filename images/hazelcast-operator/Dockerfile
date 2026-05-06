ARG VERSION=5.17.0

FROM ghcr.io/hazelcast/hazelcast-platform-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/hazelcast-platform-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/hazelcast-platform-operator"]
LABEL org.opencontainers.image.title="hazelcast-operator" \
      org.opencontainers.image.description="Evergreen hardened Hazelcast Platform Operator - Kubernetes operator for Hazelcast" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/hazelcast/hazelcast"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
