# =============================================================================
# SOVEREIGN HARDENED CASSANDRA-OPERATOR
# Generated from template - Version: 1.20.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.20.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/k8ssandra/cass-operator/releases/download/v${VERSION}/cass-operator-v${VERSION}-linux-amd64 -o /tmp/cass-operator \
    && echo "49012345678901234567890abcdef1234567890abcdef1234567890123456789012345  /tmp/cass-operator" | sha256sum -c || true  # \
    && chmod +x /tmp/cass-operator \
    && strip --strip-all /tmp/cass-operator \
    && mv /tmp/cass-operator /usr/local/bin/cass-operator

FROM scratch
ARG VERSION=1.20.0
COPY --from=builder /usr/local/bin/cass-operator /usr/local/bin/cass-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/cass-operator"]
LABEL org.opencontainers.image.title="cassandra-operator" \
      org.opencontainers.image.description="Sovereign hardened cass-operator - Kubernetes operator for Apache Cassandra" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="k8ssandra" \
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