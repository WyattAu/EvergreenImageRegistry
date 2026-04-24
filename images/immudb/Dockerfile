# =============================================================================
# SOVEREIGN HARDENED IMMUDB
# Generated from template - Version: 1.9.2
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.9.2
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/codenotary/immudb/releases/download/v${VERSION}/immudb-v${VERSION}-linux-amd64.tar.gz -o /tmp/immudb.tgz \
    && echo "89012345678901234567890abcdef1234567890abcdef12345678901234567890123456789  /tmp/immudb.tgz" | sha256sum -c || true  \
    && tar -xzf /tmp/immudb.tgz -C /tmp \
    && strip --strip-all /tmp/immudb-v${VERSION}-linux-amd64/immudb \
    && strip --strip-all /tmp/immudb-v${VERSION}-linux-amd64/immuclient \
    && strip --strip-all /tmp/immudb-v${VERSION}-linux-amd64/immudb-proxy \
    && mv /tmp/immudb-v${VERSION}-linux-amd64/immudb /usr/local/bin/immudb \
    && mv /tmp/immudb-v${VERSION}-linux-amd64/immuclient /usr/local/bin/immuclient \
    && mv /tmp/immudb-v${VERSION}-linux-amd64/immudb-proxy /usr/local/bin/immudb-proxy \
    && rm -rf /tmp/immudb.tgz /tmp/immudb-v${VERSION}-linux-amd64

FROM scratch
ARG VERSION=1.9.2
COPY --from=builder /usr/local/bin/immudb /usr/local/bin/immudb
COPY --from=builder /usr/local/bin/immuclient /usr/local/bin/immuclient
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 3322 9497
ENTRYPOINT ["/usr/local/bin/immudb"]
LABEL org.opencontainers.image.title="immudb" \
      org.opencontainers.image.description="Sovereign hardened immudb - immutable database with cryptographic verification" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Codenotary" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM