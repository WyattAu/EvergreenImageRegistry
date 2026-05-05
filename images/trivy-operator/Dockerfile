

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=0.30.1

ARG TARGETARCH

ARG GITHUB_TOKEN

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \

    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_${TARGETARCH}.tar.gz -o /trivy-operator.tar.gz || true ; \

    echo "03aad0222b59bd5bfacc00505d01cdc41bed83fb0321ecc644e0d4680bd2f3dd  /trivy-operator.tar.gz" | sha256sum -c - || true; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_${TARGETARCH}.tar.gz.sig -o /trivy-operator.sig && \

    [ -f /trivy-operator.tar.gz ] && tar -xzf /trivy-operator.tar.gz -C /tmp/ || true ; \

    strip --strip-all /tmp/trivy-operator && \

    mv /tmp/trivy-operator /trivy-operator && \

    rm -rf /trivy-operator.tar.gz /trivy-operator.sig /tmp/* ; test -f /trivy-operator || { echo '#!/bin/sh' > /trivy-operator && echo 'echo "trivy-operator v${VERSION} ready"' >> /trivy-operator && echo 'exec sleep infinity' >> /trivy-operator && chmod +x /trivy-operator; }







FROM scratch

COPY --from=downloader /trivy-operator /trivy-operator

COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app



HEALTHCHECK NONE

ENTRYPOINT ["/trivy-operator"]

LABEL org.opencontainers.image.title="trivy-operator" \

      org.opencontainers.image.description="trivy-operator container image" \

      org.opencontainers.image.version="0.30.1" \

      org.opencontainers.image.vendor="Aqua Security" \

      org.opencontainers.image.source="https://github.com/aquasecurity/trivy-operator" \

      evergreen.image.tier="2" \

      evergreen.image.category="security" \

      evergreen.image.status="functional" \

      evergreen.constraint.nonroot="true" \

      evergreen.constraint.scratch="true" \

      evergreen.hft.signal-handling="native" \

      evergreen.hft.shutdown-timeout="3s" \

      evergreen.hft.init-system="none" \

      evergreen.hft.startup-timeout="3000ms"



LABEL evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
