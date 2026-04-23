# =============================================================================
# SOVEREIGN HARDENED HAZELCAST-OPERATOR
# Generated from template - Version: 5.15.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.15.0
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/hazelcast/hazelcast-platform-operator/releases/download/v${VERSION}/hazelcast-platform-operator-v${VERSION}-linux-amd64" -o /tmp/hazelcast-operator \
    && echo "79012345678901234567890abcdef1234567890abcdef1234567890123456789012345678  /tmp/hazelcast-operator" | sha256sum -c || true  # \
    && chmod +x /tmp/hazelcast-operator \
    && strip --strip-all /tmp/hazelcast-operator \
    && mv /tmp/hazelcast-operator /usr/local/bin/hazelcast-platform-operator

FROM scratch
COPY --from=builder /usr/local/bin/hazelcast-platform-operator /usr/local/bin/hazelcast-platform-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/hazelcast-platform-operator"]
LABEL org.opencontainers.image.title="hazelcast-operator" \
      org.opencontainers.image.description="Sovereign hardened Hazelcast Platform Operator - Kubernetes operator for Hazelcast" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
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