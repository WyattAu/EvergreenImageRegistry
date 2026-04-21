# =============================================================================
# SOVEREIGN HARDENED VAULT-SECRETS
# Generated from template - Version: 1.3.0
# Constraint: debian-slim - no prebuilt binaries; built from source
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
#
# NOTE: vault-secrets-operator does not provide prebuilt binary releases.
# It is a Kubernetes operator built from source using Go.
# For production use, deploy via Helm chart instead.
# =============================================================================

ARG VERSION=1.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://go.dev/dl/go1.22.0.linux-amd64.tar.gz" | tar -C /usr/local -xzf - && rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/local/go/bin:${PATH}"
RUN git clone --depth 1 --branch v${VERSION} https://github.com/hashicorp/vault-secrets-operator.git /tmp/vso && \
    cd /tmp/vso && go build -o /vault-secrets-operator ./cmd/operator && \
    rm -rf /tmp/vso

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' vso 2>/dev/null || true
RUN mkdir -p /app /var/log/vault-secrets-operator /var/cache/vault-secrets-operator && \
    chown -R vso:vso /app /var/log/vault-secrets-operator /var/cache/vault-secrets-operator 2>/dev/null || true
COPY --from=builder /vault-secrets-operator /app/vault-secrets-operator
USER vso
WORKDIR /app
EXPOSE 8200
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/app/vault-secrets-operator", "version"]
ENTRYPOINT ["/app/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
