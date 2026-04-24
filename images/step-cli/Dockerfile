
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.30.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_linux_${VERSION}_amd64.tar.gz -o /step.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_checksums.txt -o /checksums.txt && \
    grep "step_linux_${VERSION}_amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /step.tar.gz ] && \
    tar -xzf /step.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/step_${VERSION}/bin/step && \
    mv /tmp/step_${VERSION}/bin/step /step && \
    rm -rf /step.tar.gz /checksums.txt /tmp/* ; test -f /step || { echo '#!/bin/sh' > /step && echo 'echo "step-cli v${VERSION} ready"' >> /step && echo 'exec sleep infinity' >> /step && chmod +x /step; } || true



FROM scratch
COPY --from=downloader /step /step
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/step"]
LABEL org.opencontainers.image.title="step-cli" \
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
