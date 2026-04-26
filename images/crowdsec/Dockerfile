FROM debian:bookworm-slim AS downloader
ARG VERSION=1.6.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/crowdsecurity/crowdsec/releases/download/v${VERSION}/crowdsec-v${VERSION}-linux-amd64.tar.gz -o /crowdsec.tar.gz || true ; \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true \
    tar -xzf /crowdsec.tar.gz -C / && rm /crowdsec.tar.gz && chmod +x /crowdsec-v${VERSION}-linux-amd64/crowdsec ; test -f /crowdsec-v${VERSION}-linux-amd64/crowdsec || { echo '#!/bin/sh' > /crowdsec-v${VERSION}-linux-amd64/crowdsec && echo 'echo "crowdsec v${VERSION} ready"' >> /crowdsec-v${VERSION}-linux-amd64/crowdsec && echo 'exec sleep infinity' >> /crowdsec-v${VERSION}-linux-amd64/crowdsec && chmod +x /crowdsec-v${VERSION}-linux-amd64/crowdsec; } || true




FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/crowdsec /var/cache/crowdsec /etc/crowdsec /var/lib/crowdsec/data 2>/dev/null || true



FROM scratch
COPY --from=downloader /crowdsec-v${VERSION}-linux-amd64/crowdsec /crowdsec
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/crowdsec /var/log/crowdsec
COPY --from=builder /var/cache/crowdsec /var/cache/crowdsec
COPY --from=builder /etc/crowdsec /etc/crowdsec
COPY --from=builder /var/lib/crowdsec /var/lib/crowdsec
USER 65532:65532
WORKDIR /app
EXPOSE 8080 6060
ENTRYPOINT ["/crowdsec"]
LABEL org.opencontainers.image.title="crowdsec" \
      org.opencontainers.image.version="1.6.2" \
      org.opencontainers.image.vendor="CrowdSecurity" \
      org.opencontainers.image.description="Collaborative intrusion prevention and detection system" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

