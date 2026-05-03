ARG VERSION=latest
ARG TARGETARCH

FROM grafana/vault_exporter:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/prometheus-vault-exporter /var/cache/prometheus-vault-exporter 2>/dev/null || true


FROM scratch
COPY --from=upstream /bin/vault_exporter /vault_exporter
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-vault-exporter /var/log/prometheus-vault-exporter
COPY --from=builder /var/cache/prometheus-vault-exporter /var/cache/prometheus-vault-exporter

WORKDIR /app

EXPOSE 9108
EXPOSE 9101

LABEL org.opencontainers.image.title="prometheus-vault-exporter" org.opencontainers.image.version="0.10.0" org.opencontainers.image.vendor="Prometheus Community" org.opencontainers.image.description="Prometheus exporter for HashiCorp Vault metrics" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="exclusive" evergreen.hft.deploy-strategy="hft-stateful" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/vault_exporter"]
