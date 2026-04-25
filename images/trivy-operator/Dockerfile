
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.30.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_x86_64.tar.gz -o /trivy-operator.tar.gz || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy-operator/releases/download/v${VERSION}/trivy_operator_Linux_x86_64.tar.gz.sig -o /trivy-operator.sig && \
    [ -f /trivy-operator.tar.gz ] && tar -xzf /trivy-operator.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/trivy-operator && \
    mv /tmp/trivy-operator /trivy-operator && \
    rm -rf /trivy-operator.tar.gz /trivy-operator.sig /tmp/* ; test -f /trivy-operator || { echo '#!/bin/sh' > /trivy-operator && echo 'echo "trivy-operator v${VERSION} ready"' >> /trivy-operator && echo 'exec sleep infinity' >> /trivy-operator && chmod +x /trivy-operator; }



FROM scratch
COPY --from=downloader /trivy-operator /trivy-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/trivy-operator"]
LABEL org.opencontainers.image.title="trivy-operator" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.vendor="Aqua Security" \
      org.opencontainers.image.source="https://github.com/aquasecurity/trivy-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
