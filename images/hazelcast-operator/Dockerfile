ARG VERSION=5.15.0

FROM ghcr.io/hazelcast/hazelcast-platform-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/hazelcast-platform-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/hazelcast-platform-operator"]
LABEL org.opencontainers.image.title="hazelcast-operator" \
      org.opencontainers.image.description="Sovereign hardened Hazelcast Platform Operator - Kubernetes operator for Hazelcast" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
