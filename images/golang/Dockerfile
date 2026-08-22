ARG VERSION=1.23
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# Build stage: Go toolchain on wolfi
FROM cgr.dev/chainguard/wolfi-base:1.23 AS builder
ARG VERSION
RUN apk add --no-cache go~${VERSION} git ca-certificates

# Final stage: wolfi-base with Go toolchain
FROM cgr.dev/chainguard/wolfi-base:1.23
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/bin/go /usr/bin/go
COPY --from=builder /usr/lib/go/ /usr/lib/go/
COPY --from=builder /usr/local/go/ /usr/local/go/
RUN apk add --no-cache git ca-certificates && \
    mkdir -p /go/src /go/bin /root/.cache && \
    chown -R 65532:65532 /go /root/.cache

ENV GOPATH=/go
ENV PATH="${GOPATH}/bin:/usr/local/go/bin:${PATH}"
ENV SHIM_METRICS_ENABLED="true"

USER 65532:65532
WORKDIR /go/src

EXPOSE 8080 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "go"]

LABEL org.opencontainers.image.title="golang" \
      org.opencontainers.image.description="Go toolchain - wolfi-base, non-root, with health-shim" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.source="https://go.dev" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
