# =============================================================================
# SOVEREIGN HARDENED NGINX INGRESS CONTROLLER
# Kubernetes NGINX Ingress Controller
# Constraint: scratch - Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.10.1
ARG BUILD_DATE

ARG GO_VERSION=1.22.4

FROM golang:${GO_VERSION}-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch controller-v${VERSION} \
    https://github.com/kubernetes/ingress-nginx /src && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=v${VERSION}" \
    -trimpath \
    -o /nginx-ingress-controller ./cmd/nginx

FROM debian:bookworm-slim AS certs
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim AS builder2
RUN mkdir -p /app /var/log/nginx-ingress /etc/nginx

FROM scratch
COPY --from=builder /nginx-ingress-controller /nginx-ingress-controller
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder2 /app /app
COPY --from=builder2 /var/log/nginx-ingress /var/log/nginx-ingress
COPY --from=builder2 /etc/nginx /etc/nginx
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8443
ENTRYPOINT ["/nginx-ingress-controller"]
LABEL org.opencontainers.image.title="nginx-ingress-controller" \
      org.opencontainers.image.version="1.10.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.source="https://github.com/kubernetes/ingress-nginx" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM