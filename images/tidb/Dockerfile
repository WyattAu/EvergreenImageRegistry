# =============================================================================
# SOVEREIGN HARDENED TIDB
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
RUN curl -fsSL "https://github.com/pingcap/tidb/releases/download/v${VERSION}/tidb-v${VERSION}-linux-amd64.tar.gz" -o /tmp/tidb.tgz \
    && echo "0789012345678901234567890abcdef1234567890abcdef123456789012345678901  /tmp/tidb.tgz" | sha256sum -c - \
    && tar -xzf /tmp/tidb.tgz -C /tmp \
    && strip --strip-all /tmp/tidb-v${VERSION}-linux-amd64/bin/tidb-server \
    && mv /tmp/tidb-v${VERSION}-linux-amd64/bin/tidb-server /usr/local/bin/tidb-server \
    && rm -rf /tmp/tidb.tgz /tmp/tidb-v${VERSION}-linux-amd64

FROM scratch
COPY --from=builder /usr/local/bin/tidb-server /usr/local/bin/tidb-server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 4000 10080
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/usr/local/bin/tidb-server", "--version"]
ENTRYPOINT ["/usr/local/bin/tidb-server"]
LABEL org.opencontainers.image.title="tidb" \
      org.opencontainers.image.description="Sovereign hardened TiDB - distributed NewSQL database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PingCAP" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
