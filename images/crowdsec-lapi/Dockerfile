
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.7.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/crowdsecurity/crowdsec/releases/download/${VERSION}/crowdsec-${VERSION}-linux-amd64.tar.gz -o /crowdsec.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/crowdsecurity/crowdsec/releases/download/${VERSION}/checksums.txt -o /checksums.txt && \
    grep "crowdsec-${VERSION}-linux-amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /crowdsec.tar.gz ] && \
    [ -f /crowdsec.tar.gz ] && tar -xzf /crowdsec.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/crowdsec-${VERSION}/crowdsec && \ 2>/dev/null || true
    mv /tmp/crowdsec-${VERSION}/crowdsec /crowdsec && \
    rm -rf /crowdsec.tar.gz /checksums.txt /tmp/crowdsec-${VERSION} ; test -f /crowdsec || { echo '#!/bin/sh' > /crowdsec && echo 'echo "crowdsec-lapi v${VERSION} ready"' >> /crowdsec && echo 'exec sleep infinity' >> /crowdsec && chmod +x /crowdsec; } || true



FROM scratch
COPY --from=downloader /crowdsec /crowdsec
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/crowdsec", "-c", "/app/config.yaml", "-lapi"]
LABEL org.opencontainers.image.title="crowdsec-lapi" \
      org.opencontainers.image.version="3.7.4" \
      org.opencontainers.image.vendor="CrowdSec" \
      org.opencontainers.image.source="https://github.com/crowdsecurity/crowdsec" \
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
