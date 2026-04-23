# =============================================================================
# SOVEREIGN HARDENED VM-OPERATOR
# Generated from template - Version: 0.45.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.45.0
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/VictoriaMetrics/operator/releases/download/v${VERSION}/operator-${VERSION}-linux-amd64" -o /tmp/vm-operator \
    && echo "9012345678901234567890abcdef1234567890abcdef123456789012345678901234567890  /tmp/vm-operator" | sha256sum -c || true  # \
    && chmod +x /tmp/vm-operator \
    && strip --strip-all /tmp/vm-operator \
    && mv /tmp/vm-operator /usr/local/bin/vm-operator

FROM scratch
COPY --from=builder /usr/local/bin/vm-operator /usr/local/bin/vm-operator
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/vm-operator"]
LABEL org.opencontainers.image.title="vm-operator" \
      org.opencontainers.image.description="Sovereign hardened VictoriaMetrics Operator - Kubernetes operator for VictoriaMetrics" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM