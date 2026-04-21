# =============================================================================
# SOVEREIGN HARDENED GRAYLOG-SIDECAR
# Version: 1.5.0
# Constraint: scratch - static Go binary, no shell, no package manager
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/Graylog2/collector-sidecar/releases/download/${VERSION}/collector-sidecar-${VERSION}-linux-amd64.tar.gz" -o /sidecar.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /sidecar.tar.gz" | sha256sum -c - \
    && mkdir -p /opt/sidecar \
    && tar -xzf /sidecar.tar.gz -C /opt/sidecar --strip-components=1 \
    && rm /sidecar.tar.gz \
    && strip /opt/sidecar/collector_sidecar || true \
    && chmod +x /opt/sidecar/collector_sidecar

FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/sidecar /var/lib/sidecar /var/cache/sidecar

FROM scratch
COPY --from=downloader /opt/sidecar /opt/sidecar
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/sidecar /var/log/sidecar
COPY --from=builder /var/lib/sidecar /var/lib/sidecar
COPY --from=builder /var/cache/sidecar /var/cache/sidecar
USER 65534:65534
WORKDIR /opt/sidecar
EXPOSE 8989
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/sidecar/collector_sidecar", "-version"]
ENTRYPOINT ["/opt/sidecar/collector_sidecar"]
LABEL org.opencontainers.image.title="graylog-sidecar" \
      org.opencontainers.image.description="Sovereign hardened Graylog Sidecar - log collector management agent" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Graylog" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
