FROM debian:bookworm-slim AS downloader
ARG VERSION=1.7.7
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/crowdsecurity/crowdsec/releases/download/v${VERSION}/crowdsec-release.tgz" \
    -o /crowdsec-release.tgz && \
    tar -xzf /crowdsec-release.tgz -C /tmp/ && \
    cp /tmp/crowdsec-v${VERSION}/cmd/crowdsec/crowdsec /crowdsec && \
    chmod +x /crowdsec && \
    strip --strip-all /crowdsec && \
    rm -rf /crowdsec-release.tgz /tmp/crowdsec-v${VERSION}

FROM scratch
COPY --from=downloader /crowdsec /crowdsec
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 6060
ENTRYPOINT ["/crowdsec"]
CMD ["-c /app/config.yaml -t"]
LABEL org.opencontainers.image.title="crowdsec-agent"       org.opencontainers.image.version="1.7.7"       org.opencontainers.image.vendor="CrowdSecurity"       org.opencontainers.image.source="https://github.com/crowdsecurity/crowdsec"       sovereign.image.tier="1"       sovereign.image.category="security"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
