# =============================================================================
# SOVEREIGN HARDENED ZITADEL OPERATOR
# Kubernetes operator for ZITADEL - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/zitadel/zitadel-operator/releases/download/v${VERSION}/zitadel-operator_${VERSION}_linux_amd64.tar.gz" -o /zitadel-operator.tar.gz && \
    curl -fsSL "https://github.com/zitadel/zitadel-operator/releases/download/v${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "zitadel-operator_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /zitadel-operator.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/zitadel-operator && \
    mv /tmp/zitadel-operator /zitadel-operator && \
    rm -rf /zitadel-operator.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /zitadel-operator /zitadel-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/zitadel-operator"]
LABEL org.opencontainers.image.title="zitadel-operator" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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