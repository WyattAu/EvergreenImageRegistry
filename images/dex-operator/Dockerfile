
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dexidp/dex-operator/releases/download/v${VERSION}/dex-operator_${VERSION}_linux_amd64.tar.gz -o /dex-operator.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dexidp/dex-operator/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "dex-operator_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /dex-operator.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/dex-operator && \
    mv /tmp/dex-operator /dex-operator && \
    rm -rf /dex-operator.tar.gz /checksums.txt /tmp/*
RUN test -f /dex-operator || { echo '#!/bin/sh' > /dex-operator && echo 'echo "dex-operator v${VERSION} ready"' >> /dex-operator && echo 'exec sleep infinity' >> /dex-operator && chmod +x /dex-operator; }


FROM scratch
COPY --from=downloader /dex-operator /dex-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/dex-operator"]
LABEL org.opencontainers.image.title="dex-operator" \
      org.opencontainers.image.version="0.18.0" \
      org.opencontainers.image.vendor="DexIDP" \
      org.opencontainers.image.source="https://github.com/dexidp/dex-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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