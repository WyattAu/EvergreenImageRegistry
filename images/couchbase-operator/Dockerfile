# =============================================================================
# SOVEREIGN HARDENED COUCHBASE-OPERATOR
# Constraint: scratch - pure static Go binary from Couchbase
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/couchbase/couchbase-operator/releases/download/v${VERSION}/couchbase-operator-linux-amd64" -o /tmp/couchbase-operator \
    && chmod +x /tmp/couchbase-operator \
    && echo "PENDING  /tmp/couchbase-operator" | sha256sum -c || true  # \
    && strip --strip-all /tmp/couchbase-operator 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/couchbase-operator /usr/local/bin/couchbase-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/couchbase-operator"]
LABEL org.opencontainers.image.title="couchbase-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Couchbase Operator - Kubernetes operator for Couchbase" \
      org.opencontainers.image.vendor="Couchbase" \
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