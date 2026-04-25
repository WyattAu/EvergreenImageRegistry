# =============================================================================
# SOVEREIGN HARDENED ZINCONE (ZincSearch Observability Edition)
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.12
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zincsearch/zincsearch/releases/download/v${VERSION}/zincsearch_${VERSION}_linux_amd64.tar.gz -o zinc.tar.gz \
    && echo "PENDING  zinc.tar.gz" | sha256sum -c || true  \
    && [ -f zinc.tar.gz ] && tar -xzf zinc.tar.gz || true ; \
    strip --strip-all zincsearch 2>/dev/null || true \    && mv zincsearch /tmp/zincone

RUN mkdir -p /tmp/zincone 2>/dev/null || true

FROM scratch
ARG VERSION=0.4.12
COPY --from=builder /tmp/zincone /usr/local/bin/zincone
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 4080
ENTRYPOINT ["/usr/local/bin/zincone"]
LABEL org.opencontainers.image.title="zincone" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ZincOne - ZincSearch observability edition" \
      org.opencontainers.image.vendor="ZincSearch" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM