# =============================================================================
# SOVEREIGN HARDENED CROWDSEC AGENT
# CrowdSec security agent - agent-mode entrypoint
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=v3.7.4
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/crowdsecurity/crowdsec/releases/download/${VERSION}/crowdsec-${VERSION}-linux-amd64.tar.gz" -o /crowdsec.tar.gz && \
    curl -fsSL "https://github.com/crowdsecurity/crowdsec/releases/download/${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "crowdsec-${VERSION}-linux-amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /crowdsec.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/crowdsec-${VERSION}/crowdsec && \
    mv /tmp/crowdsec-${VERSION}/crowdsec /crowdsec && \
    rm -rf /crowdsec.tar.gz /checksums.txt /tmp/crowdsec-${VERSION}

FROM scratch
COPY --from=downloader /crowdsec /crowdsec
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/crowdsec", "-version"]
ENTRYPOINT ["/crowdsec", "-c", "/app/config.yaml", "-t"]
LABEL org.opencontainers.image.title="crowdsec-agent" \
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
