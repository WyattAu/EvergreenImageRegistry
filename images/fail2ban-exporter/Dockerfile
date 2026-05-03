FROM golang:1.22-alpine AS builder
ARG TARGETARCH
ARG VERSION=v0.10.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN apk add --no-cache git
RUN git clone --depth 1 --branch ${VERSION} https://github.com/xperimental/fail2ban-exporter.git /src 2>/dev/null || \
    git clone --depth 1 https://github.com/xperimental/fail2ban-exporter.git /src
WORKDIR /src
RUN CGO_ENABLED=0 GOARCH=${GOARCH} go build -o /fail2ban-exporter .

FROM scratch
COPY --from=builder /fail2ban-exporter /fail2ban-exporter
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9191
ENTRYPOINT ["/fail2ban-exporter"]
CMD ["--web.listen-address=:9191", "--web.telemetry-path=/metrics", "--fail2ban.socket=/tmp/fail2ban.sock"]
LABEL org.opencontainers.image.title="fail2ban-exporter"       org.opencontainers.image.version="v0.10.0"       org.opencontainers.image.vendor="xperimental"       org.opencontainers.image.source="https://github.com/xperimental/fail2ban-exporter"       sovereign.image.tier="1"       sovereign.image.category="monitoring"       sovereign.image.status="best-effort"       sovereign.image.note="Original repo deleted; building from source"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
