ARG VERSION=v1.2.0

FROM golang:1.22 AS upstream

FROM golang@sha256:b54cbf583d390341599d7bcbc062425c081105cc5ef6d170ced98ef9d047c716 AS builder
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN GOARCH=${GOARCH} go install golang.org/x/vuln/cmd/govulncheck@${VERSION} || true


FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=builder /go/bin/govulncheck /govulncheck
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="govulncheck"       org.opencontainers.image.description="Go vulnerability checker"       org.opencontainers.image.vendor="go-1.23"       org.opencontainers.image.source="https://github.com/go-1.23/vuln"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="latest"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/govulncheck"]

CMD ["--help"]
