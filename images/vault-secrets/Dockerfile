ARG VERSION=latest

FROM hashicorp/vault-secrets-operator:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vault-secrets /var/cache/vault-secrets 2>/dev/null || true


FROM scratch
COPY --from=upstream /vault-secrets-operator /vault-secrets-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault-secrets /var/log/vault-secrets
COPY --from=builder /var/cache/vault-secrets /var/cache/vault-secrets

WORKDIR /app

EXPOSE 8080 8443
EXPOSE 9101

LABEL org.opencontainers.image.title="vault-secrets" org.opencontainers.image.version="1.4.0" org.opencontainers.image.vendor="HashiCorp" org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" sovereign.image.tier="1" sovereign.image.category="security" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/vault-secrets-operator"]
