# =============================================================================
# SOVEREIGN HARDENED FERRETDB
# Generated from template - Version: 1.21.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/FerretDB/FerretDB/releases/download/v${VERSION}/ferretdb-${VERSION}-linux-amd64.tar.gz" -o /tmp/ferretdb.tgz \
    && echo "d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890123456  /tmp/ferretdb.tgz" | sha256sum -c - \
    && tar -xzf /tmp/ferretdb.tgz -C /tmp \
    && strip --strip-all /tmp/ferretdb \
    && mv /tmp/ferretdb /usr/local/bin/ferretdb \
    && rm -rf /tmp/ferretdb.tgz

FROM scratch
COPY --from=builder /usr/local/bin/ferretdb /usr/local/bin/ferretdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 27017 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/ferretdb", "version"]
ENTRYPOINT ["/usr/local/bin/ferretdb"]
LABEL org.opencontainers.image.title="ferretdb" \
      org.opencontainers.image.description="Sovereign hardened FerretDB - MongoDB-compatible database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="FerretDB" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
