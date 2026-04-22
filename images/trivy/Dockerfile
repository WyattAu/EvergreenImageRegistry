# =============================================================================
# SOVEREIGN HARDENED TRIVY
# Vulnerability scanner - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.70.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_Linux-64bit.tar.gz" -o /trivy.tar.gz && \
    curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_checksums.txt" -o /checksums.txt && \
    grep "trivy_${VERSION}_Linux-64bit.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /trivy.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/trivy && \
    mv /tmp/trivy /trivy && \
    rm -rf /trivy.tar.gz /checksums.txt /tmp/*

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/trivy /var/cache/trivy

FROM scratch
COPY --from=downloader /trivy /trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/trivy /var/log/trivy
COPY --from=builder /var/cache/trivy /var/cache/trivy
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/trivy", "version"]
ENTRYPOINT ["/trivy"]
LABEL org.opencontainers.image.title="trivy" \
      org.opencontainers.image.version="0.70.0" \
      org.opencontainers.image.vendor="Aqua Security" \
      org.opencontainers.image.source="https://github.com/aquasecurity/trivy" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
