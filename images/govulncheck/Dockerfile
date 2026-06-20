ARG VERSION=v1.1.4
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang:1.24@sha256:46fdd02b6cbcd624a4087ea298e4c8505e5d400c4ee5181e4dd06e2297d647ae AS builder
ENV GOTOOLCHAIN=auto
ARG VERSION
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN GOARCH=${GOARCH} go install golang.org/x/vuln/cmd/govulncheck@${VERSION}


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
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
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/govulncheck"]

CMD ["--help"]
