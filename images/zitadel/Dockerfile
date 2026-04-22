# =============================================================================
# SOVEREIGN HARDENED ZITADEL
# Identity and access management - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.13.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/zitadel/zitadel/releases/download/v${VERSION}/zitadel-linux-amd64.tar.gz" -o /zitadel.tar.gz && \
    curl -fsSL "https://github.com/zitadel/zitadel/releases/download/v${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "zitadel-linux-amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /zitadel.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/zitadel && \
    mv /tmp/zitadel /zitadel && \
    rm -rf /zitadel.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /zitadel /zitadel
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/zitadel", "version"]
ENTRYPOINT ["/zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.version="4.13.1" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
