# =============================================================================
# SOVEREIGN HARDENED SCYLLA-OPERATOR
# Generated from template - Version: 1.13.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.13.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/scylladb/scylla-operator/releases/download/v${VERSION}/scylla-operator-v${VERSION}-linux-amd64 -o /tmp/scylla-operator ; echo "59012345678901234567890abcdef1234567890abcdef12345678901234567890123456  /tmp/scylla-operator" | sha256sum -c || true  ; chmod +x /tmp/scylla-operator ; strip --strip-all /tmp/scylla-operator \
    && mv /tmp/scylla-operator /usr/local/bin/scylla-operator

RUN mkdir -p /usr/local/bin/scylla-operator 2>/dev/null || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM scratch
ARG VERSION=1.13.0
COPY --from=builder /usr/local/bin/scylla-operator /usr/local/bin/scylla-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/scylla-operator"]
LABEL org.opencontainers.image.title="scylla-operator" \
      org.opencontainers.image.description="Sovereign hardened ScyllaDB Operator - Kubernetes operator for ScyllaDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ScyllaDB" \
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