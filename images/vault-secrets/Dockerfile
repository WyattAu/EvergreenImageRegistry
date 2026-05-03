ARG VERSION=latest

FROM hashicorp/vault-secrets-operator:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="vault-secrets" org.opencontainers.image.version="1.4.0" org.opencontainers.image.vendor="HashiCorp" org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" evergreen.image.tier="1" evergreen.image.category="security" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/vault-secrets-operator"]
