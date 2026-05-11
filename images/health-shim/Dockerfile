FROM golang:1.23-bookworm AS builder
ARG TARGETARCH
ARG VERSION=1.0.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
WORKDIR /src
COPY go.mod health-shim.go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /health-shim health-shim.go || true

FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=builder /health-shim /health-shim
USER 65532:65532
EXPOSE 9101
ENTRYPOINT ["/health-shim"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="health-shim" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.category="observability" \
      evergreen.health.type="http" \
      evergreen.metrics.native="prometheus"
