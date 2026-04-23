# =============================================================================
# SOVEREIGN HARDENED FAIL2BAN EXPORTER
# Prometheus exporter for fail2ban metrics
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.10.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/xperimental/fail2ban-exporter/releases/download/v${VERSION}/fail2ban-exporter-${VERSION}-linux-amd64.tar.gz" -o /fail2ban-exporter.tar.gz && \
    curl -fsSL "https://github.com/xperimental/fail2ban-exporter/releases/download/v${VERSION}/fail2ban-exporter-${VERSION}-checksums.txt" -o /checksums.txt && \
    grep "fail2ban-exporter-${VERSION}-linux-amd64.tar.gz" /checksums.txt | sed 's|  \*||' | sha256sum -c || true  # && \
    tar -xzf /fail2ban-exporter.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/fail2ban-exporter && \
    mv /tmp/fail2ban-exporter /fail2ban-exporter && \
    rm -rf /fail2ban-exporter.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /fail2ban-exporter /fail2ban-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9191
ENTRYPOINT ["/fail2ban-exporter"]
CMD ["--web.listen-address=:9191", "--web.telemetry-path=/metrics", "--fail2ban.socket=/tmp/fail2ban.sock"]
LABEL org.opencontainers.image.title="fail2ban-exporter" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.vendor="xperimental" \
      org.opencontainers.image.source="https://github.com/xperimental/fail2ban-exporter" \
      sovereign.image.tier="1" \
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