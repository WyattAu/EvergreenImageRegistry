ARG VERSION=v1.1.4
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang:1.24 AS builder
ENV GOTOOLCHAIN=auto
ARG VERSION
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN GOARCH=${GOARCH} go install golang.org/x/vuln/cmd/govulncheck@${VERSION}


FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=builder /go/bin/govulncheck /govulncheck
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="govulncheck"       org.opencontainers.image.description="Go vulnerability checker"       org.opencontainers.image.vendor="golang"       org.opencontainers.image.source="https://github.com/golang/vuln"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="v1.1.4"
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
