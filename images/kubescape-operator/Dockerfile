ARG VERSION=latest

FROM ghcr.io/kubescape/kubescape-operator:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kubescape-operator /var/cache/kubescape-operator 2>/dev/null || true


FROM scratch
COPY --from=upstream /kubescape /usr/local/bin/kubescape
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kubescape-operator /var/log/kubescape-operator
COPY --from=builder /var/cache/kubescape-operator /var/cache/kubescape-operator

WORKDIR /app

EXPOSE 9101

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE

LABEL org.opencontainers.image.description="kubescape-operator container image" \
      org.opencontainers.image.title="Kubescape Operator" \
      org.opencontainers.image.source="https://github.com/kubescape/kubescape" \
            org.opencontainers.image.version="latest"

ENTRYPOINT ["/kubescape"]

CMD ["--help"]
