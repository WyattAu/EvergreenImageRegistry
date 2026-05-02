ARG VERSION=latest

FROM ghcr.io/kubescape/kubescape-operator:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubescape-operator /var/cache/kubescape-operator 2>/dev/null || true


FROM scratch
COPY --from=upstream /kubescape /usr/local/bin/kubescape
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kubescape-operator /var/log/kubescape-operator
COPY --from=builder /var/cache/kubescape-operator /var/cache/kubescape-operator

WORKDIR /app

EXPOSE 9101

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/kubescape"]

CMD ["--help"]
