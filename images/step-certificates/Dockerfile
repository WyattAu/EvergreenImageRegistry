# =============================================================================
# SOVEREIGN HARDENED STEP CERTIFICATES
# Smallstep online CA for automated certificate management - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.30.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/smallstep/certificates/releases/download/v${VERSION}/step-ca_linux_${VERSION}_amd64.tar.gz" -o /step-ca.tar.gz && \
    curl -fsSL "https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_checksums.txt" -o /checksums.txt && \
    grep "step-ca_linux_${VERSION}_amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /step-ca.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/step-ca && \
    mv /tmp/step-ca /step-ca && \
    rm -rf /step-ca.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /step-ca /step-ca
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/step-ca", "--version"]
ENTRYPOINT ["/step-ca"]
LABEL org.opencontainers.image.title="step-certificates" \
      org.opencontainers.image.version="0.30.2" \
      org.opencontainers.image.vendor="Smallstep" \
      org.opencontainers.image.source="https://github.com/smallstep/certificates" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
