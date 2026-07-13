ARG APP_UID=65532
ARG APP_GID=65532
ARG VERSION=1.2.0

FROM golang:1.23-bookworm@sha256:e87b2a5f6df2dff71ea330d55d54f4979eb380ae58a7e3aabc9d53121243e689 AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -trimpath \
    -ldflags="-s -w -X main.version=${VERSION}" -o /shim .

FROM scratch
ARG APP_UID
ARG APP_GID
ARG VERSION
LABEL org.opencontainers.image.title="health-shim" \
      org.opencontainers.image.version="${VERSION}" \
      evergreen.image.category="observability" \
      evergreen.health.type="http" \
      evergreen.metrics.native="prometheus"
COPY --from=builder /shim /shim
USER ${APP_UID}:${APP_GID}
EXPOSE 9101
ENTRYPOINT ["/usr/local/bin/shim"]
LABEL evergreen.entrypoint.pattern="base-image"
LABEL evergreen.image.tier="standard"
STOPSIGNAL SIGTERM
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
