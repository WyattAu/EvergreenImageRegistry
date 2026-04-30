FROM golang:1.23-bookworm AS builder
ARG VERSION=1.0.0
WORKDIR /src
COPY health-shim.go .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /health-shim .

FROM scratch
COPY --from=builder /health-shim /health-shim
USER 65532:65532
EXPOSE 9101
ENTRYPOINT ["/health-shim"]
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="health-shim" \
      org.opencontainers.image.version="${VERSION}" \
      sovereign.image.category="observability" \
      sovereign.health.type="http" \
      sovereign.metrics.native="prometheus"
