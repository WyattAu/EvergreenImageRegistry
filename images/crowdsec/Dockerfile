# =============================================================================
# SOVEREIGN HARDENED CROWDSEC
# Version: 1.6.2
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=1.6.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/crowdsecurity/crowdsec/releases/download/v${VERSION}/crowdsec-v${VERSION}-linux-amd64.tar.gz" -o /crowdsec.tar.gz && \
    tar -xzf /crowdsec.tar.gz -C / && rm /crowdsec.tar.gz && chmod +x /crowdsec-v${VERSION}-linux-amd64/crowdsec

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/crowdsec /var/cache/crowdsec /etc/crowdsec /var/lib/crowdsec/data

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