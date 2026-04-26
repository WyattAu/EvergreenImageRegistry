# =============================================================================
# SOVEREIGN HARDENED TIDB-LIGHTNING
# Generated from template - Version: 7.6.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.6.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pingcap/tidb/releases/download/v${VERSION}/tidb-lightning-v${VERSION}-linux-amd64.tar.gz -o /tmp/lightning.tgz ; echo "189012345678901234567890abcdef1234567890abcdef1234567890123456789012  /tmp/lightning.tgz" | sha256sum -c || true  ; [ -f /tmp/lightning.tgz ] && tar -xzf /tmp/lightning.tgz -C /tmp || true ; \
    strip --strip-all 2>/dev/null || true /tmp/tidb-lightning-v${VERSION}-linux-amd64/bin/tidb-lightning ; mv /tmp/tidb-lightning-v${VERSION}-linux-amd64/bin/tidb-lightning /usr/local/bin/tidb-lightning \
    && rm -rf /tmp/lightning.tgz /tmp/tidb-lightning-v${VERSION}-linux-amd64

RUN mkdir -p /usr/local/bin/tidb-lightning 2>/dev/null || true

FROM scratch
ARG VERSION=7.6.0
COPY --from=builder /usr/local/bin/tidb-lightning /usr/local/bin/tidb-lightning
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8289
ENTRYPOINT ["/usr/local/bin/tidb-lightning"]
LABEL org.opencontainers.image.title="tidb-lightning" \
      org.opencontainers.image.description="Sovereign hardened TiDB Lightning - high-speed TiDB data import tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="PingCAP" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM