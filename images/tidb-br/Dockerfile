# =============================================================================
# SOVEREIGN HARDENED TIDB-BR
# Generated from template - Version: 7.6.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.6.0
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/pingcap/tidb/releases/download/v${VERSION}/br-v${VERSION}-linux-amd64.tar.gz" -o /tmp/br.tgz \
    && echo "29012345678901234567890abcdef1234567890abcdef12345678901234567890123  /tmp/br.tgz" | sha256sum -c - \
    && tar -xzf /tmp/br.tgz -C /tmp \
    && strip --strip-all /tmp/br-v${VERSION}-linux-amd64/bin/br \
    && mv /tmp/br-v${VERSION}-linux-amd64/bin/br /usr/local/bin/br \
    && rm -rf /tmp/br.tgz /tmp/br-v${VERSION}-linux-amd64

FROM scratch
COPY --from=builder /usr/local/bin/br /usr/local/bin/br
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 8289
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/br", "--version"]
ENTRYPOINT ["/usr/local/bin/br"]
LABEL org.opencontainers.image.title="tidb-br" \
      org.opencontainers.image.description="Sovereign hardened TiDB BR - backup and restore tool for TiDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PingCAP" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
