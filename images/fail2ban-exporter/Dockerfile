FROM golang@sha256:1699c10032ca2582ec89a24a1312d986a3f094aed3d5c1147b19880afe40e052 AS builder

ARG TARGETARCH

ARG VERSION=v0.10.0

ARG TARGETARCH

ARG GOARCH=${TARGETARCH}

RUN apk add --no-cache git && \
    git clone --branch ${VERSION} https://github.com/xperimental/fail2ban-exporter.git /src 2>/dev/null || \
    git clone https://github.com/xperimental/fail2ban-exporter.git /src

WORKDIR /src

RUN CGO_ENABLED=0 GOARCH=${GOARCH} go build -o /fail2ban-exporter .



FROM scratch

COPY --from=builder /fail2ban-exporter /fail2ban-exporter

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app

EXPOSE 9191



HEALTHCHECK NONE

ENTRYPOINT ["/fail2ban-exporter"]

CMD ["--web.listen-address=:9191", "--web.telemetry-path=/metrics", "--fail2ban.socket=/tmp/fail2ban.sock"]

LABEL org.opencontainers.image.title="fail2ban-exporter"       org.opencontainers.image.version="v0.10.0"       org.opencontainers.image.vendor="xperimental"       org.opencontainers.image.source="https://github.com/xperimental/fail2ban-exporter"       evergreen.image.tier="1"       evergreen.image.category="monitoring"       evergreen.image.status="best-effort"       evergreen.image.note="Original repo deleted; building from source"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="fail2ban-exporter container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
