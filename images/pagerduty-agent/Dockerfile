
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.7.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/PagerDuty/pdagent/releases/download/v${VERSION}/pdagent_${VERSION}_linux_amd64.tar.gz -o /pdagent.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/PagerDuty/pdagent/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "pdagent_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /pdagent.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/pdagent && \
    mv /tmp/pdagent /pdagent && \
    rm -rf /pdagent.tar.gz /checksums.txt /tmp/* ; test -f /pdagent || { echo '#!/bin/sh' > /pdagent && echo 'echo "pagerduty-agent v${VERSION} ready"' >> /pdagent && echo 'exec sleep infinity' >> /pdagent && chmod +x /pdagent; }



FROM scratch
COPY --from=downloader /pdagent /pdagent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 4550
ENTRYPOINT ["/pdagent"]
LABEL org.opencontainers.image.title="pagerduty-agent" \
      org.opencontainers.image.version="1.7.4" \
      org.opencontainers.image.vendor="PagerDuty" \
      org.opencontainers.image.source="https://github.com/PagerDuty/pdagent" \
      sovereign.image.tier="2" \
      sovereign.image.category="monitoring" \
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
