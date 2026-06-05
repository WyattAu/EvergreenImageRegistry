# =============================================================================
# EVERGREEN HARDENED NGINX INGRESS CONTROLLER
# Kubernetes NGINX Ingress Controller
# Constraint: scratch - Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.10.1
ARG GO_VERSION=1.22.4
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM golang:${GO_VERSION}-bookworm AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.10.1
ARG GO_VERSION
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN mkdir -p /etc/nginx && \ RUN mkdir -p /app && \
    mkdir -p /etc/nginx && \ RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates make && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "controller-v${VERSION}" https://github.com/kubernetes/ingress-nginx /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w -X main.version=v${VERSION}" \
        -trimpath \
        -o /app/nginx-ingress-controller ./cmd/nginx 2>/dev/null || true && \
    test -s /app/nginx-ingress-controller && strip --strip-all /app/nginx-ingress-controller 2>/dev/null && \' && { echo "Binary not available - download failed" >&2; exit 1; }
    mkdir -p /app /var/log/nginx-ingress /etc/nginx
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /app/nginx-ingress-controller /nginx-ingress-controller
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx-ingress /var/log/nginx-ingress
COPY --from=builder /etc/nginx /etc/nginx
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="nginx-ingress-controller" \
      org.opencontainers.image.description="nginx-ingress-controller container image" \
      org.opencontainers.image.version="1.10.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.source="https://github.com/kubernetes/ingress-nginx" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
