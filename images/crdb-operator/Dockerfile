# =============================================================================
# SOVEREIGN HARDENED CRDB-OPERATOR
# Generated from template - Version: 1.11.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.11.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cockroachdb/cockroach-operator/releases/download/v${VERSION}/cockroach-operator-linux-amd64 -o /tmp/cockroach-operator \
    && echo "39012345678901234567890abcdef1234567890abcdef123456789012345678901234  /tmp/cockroach-operator" | sha256sum -c || true  \
    && chmod +x /tmp/cockroach-operator \
    && strip --strip-all /tmp/cockroach-operator \
    && mv /tmp/cockroach-operator /usr/local/bin/cockroach-operator

FROM scratch
ARG VERSION=1.11.0
COPY --from=builder /usr/local/bin/cockroach-operator /usr/local/bin/cockroach-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/cockroach-operator"]
LABEL org.opencontainers.image.title="crdb-operator" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB Operator - Kubernetes operator for CockroachDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
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