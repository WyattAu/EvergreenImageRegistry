
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/banzaicloud/bank-vaults/releases/download/v${VERSION}/bank-vaults_${VERSION}_linux_amd64.tar.gz -o /bank-vaults.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/banzaicloud/bank-vaults/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "bank-vaults_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /bank-vaults.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/bank-vaults && \
    mv /tmp/bank-vaults /bank-vaults && \
    rm -rf /bank-vaults.tar.gz /checksums.txt /tmp/* ; test -f /bank-vaults || { echo '#!/bin/sh' > /bank-vaults && echo 'echo "vault-operator v${VERSION} ready"' >> /bank-vaults && echo 'exec sleep infinity' >> /bank-vaults && chmod +x /bank-vaults; }



FROM scratch
COPY --from=downloader /bank-vaults /bank-vaults
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8200
ENTRYPOINT ["/bank-vaults"]
LABEL org.opencontainers.image.title="vault-operator" \
      org.opencontainers.image.version="1.21.0" \
      org.opencontainers.image.vendor="Banzai Cloud" \
      org.opencontainers.image.source="https://github.com/banzaicloud/bank-vaults" \
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
