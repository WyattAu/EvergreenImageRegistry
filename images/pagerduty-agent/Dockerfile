# =============================================================================
# SOVEREIGN HARDENED PAGERDUTY AGENT
# PagerDuty event relay agent - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.7.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/PagerDuty/pdagent/releases/download/v${VERSION}/pdagent_${VERSION}_linux_amd64.tar.gz" -o /pdagent.tar.gz && \
    curl -fsSL "https://github.com/PagerDuty/pdagent/releases/download/v${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "pdagent_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /pdagent.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/pdagent && \
    mv /tmp/pdagent /pdagent && \
    rm -rf /pdagent.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /pdagent /pdagent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 4550
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/pdagent", "--help"]
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
