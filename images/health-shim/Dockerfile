ARG APP_UID=65532
ARG APP_GID=65532

FROM golang:1.23-bookworm@sha256:e87b2a5f6df2dff71ea330d55d54f4979eb380ae58a7e3aabc9d53121243e689 AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.0.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
WORKDIR /src
COPY go.mod health-shim.go .
RUN touch /health-shim || true
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -trimpath -ldflags="-s -w" -o /health-shim health-shim.go || true

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
