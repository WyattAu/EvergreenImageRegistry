ARG VERSION=latest

FROM golang:${VERSION} AS upstream

FROM golang:latest AS builder
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN GOARCH=${GOARCH} go install golang.org/x/vuln/cmd/govulncheck@latest


FROM scratch
COPY --from=builder /go/bin/govulncheck /govulncheck
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="govulncheck"       org.opencontainers.image.description="Go vulnerability checker"       org.opencontainers.image.vendor="go-1.23"       org.opencontainers.image.source="https://github.com/go-1.23/vuln"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/govulncheck"]

CMD ["--help"]
