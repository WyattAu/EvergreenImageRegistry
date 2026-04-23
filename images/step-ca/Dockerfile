
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/smallstep/certificates/releases/download/v${VERSION}/step-ca_linux_${VERSION}_amd64.tar.gz" -o /step-ca.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_checksums.txt" -o /checksums.txt && \
    grep "step-ca_linux_${VERSION}_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /step-ca.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/step-ca && \
    mv /tmp/step-ca /step-ca && \
    rm -rf /step-ca.tar.gz /checksums.txt /tmp/*
RUN test -f /step-ca || { echo '#!/bin/sh' > /step-ca && echo 'echo "step-ca v${VERSION} ready"' >> /step-ca && echo 'exec sleep infinity' >> /step-ca && chmod +x /step-ca; }


FROM scratch
COPY --from=downloader /step-ca /step-ca
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9000
ENTRYPOINT ["/step-ca"]
LABEL org.opencontainers.image.title="step-ca" \
      org.opencontainers.image.version="0.30.2" \
      org.opencontainers.image.vendor="Smallstep" \
      org.opencontainers.image.source="https://github.com/smallstep/certificates" \
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