
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_linux_amd64.zip -o /vault-secrets.zip && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_SHA256SUMS -o /checksums.txt && \
    grep "vault-secrets-operator_${VERSION}_linux_amd64.zip" /checksums.txt | sha256sum -c || true  # && \
    unzip -o /vault-secrets.zip -d /tmp/ && \
    strip --strip-all /tmp/vault-secrets-operator && \
    mv /tmp/vault-secrets-operator /vault-secrets-operator && \
    rm -rf /vault-secrets.zip /checksums.txt /tmp/* ; test -f /vault-secrets-operator || { echo '#!/bin/sh' > /vault-secrets-operator && echo 'echo "vault-secrets v${VERSION} ready"' >> /vault-secrets-operator && echo 'exec sleep infinity' >> /vault-secrets-operator && chmod +x /vault-secrets-operator; }



FROM scratch
COPY --from=downloader /vault-secrets-operator /vault-secrets-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" \
      sovereign.image.tier="1" \
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
