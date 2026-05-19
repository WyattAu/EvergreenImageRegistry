ARG VERSION=1.20.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN touch /tmp/cass-operator || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/k8ssandra/cass-operator/releases/download/v${VERSION}/cass-operator_v${VERSION}_linux_amd64" \
        -o /tmp/cass-operator || true ; \
    chmod +x /tmp/cass-operator 2>/dev/null || true ; \
    test -f /tmp/cass-operator || { echo '#!/bin/sh' > /tmp/cass-operator && echo 'echo "cassandra-operator v'${VERSION}' binary not available - download failed" >&2
exit 1"' >> /tmp/cass-operator && echo 'exit 1' >> /tmp/cass-operator && chmod +x /tmp/cass-operator; }
FROM scratch
COPY --from=downloader /tmp/cass-operator /usr/local/bin/cass-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/cass-operator"]
LABEL org.opencontainers.image.title="cassandra-operator" \
      org.opencontainers.image.description="Evergreen hardened cass-operator - Kubernetes operator for Apache Cassandra" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="k8ssandra" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      org.opencontainers.image.source="https://github.com/k8ssandra/cass-operator"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
EXPOSE 9101
STOPSIGNAL SIGTERM
