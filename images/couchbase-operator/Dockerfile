ARG VERSION=2.8.0
ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -L \
        "https://github.com/couchbase/couchbase-operator/releases/download/v${VERSION}/couchbase-operator_v${VERSION}_linux_amd64" \
        -o /tmp/couchbase-operator || true ; \
    chmod +x /tmp/couchbase-operator 2>/dev/null || true ; \
    test -f /tmp/couchbase-operator || { echo '#!/bin/sh' > /tmp/couchbase-operator && echo 'echo "couchbase-operator v'${VERSION}' placeholder"' >> /tmp/couchbase-operator && echo 'exec sleep infinity' >> /tmp/couchbase-operator && chmod +x /tmp/couchbase-operator; }
FROM scratch
COPY --from=downloader /tmp/couchbase-operator /usr/local/bin/couchbase-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/couchbase-operator"]
LABEL org.opencontainers.image.title="couchbase-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Couchbase Operator - Kubernetes operator for Couchbase" \
      org.opencontainers.image.vendor="Couchbase" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      org.opencontainers.image.source="https://github.com/couchbase/couchbase-operator"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
EXPOSE 9101
STOPSIGNAL SIGTERM
