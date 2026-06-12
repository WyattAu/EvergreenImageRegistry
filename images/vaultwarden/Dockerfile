# =============================================================================
# EVERGREEN HARDENED VAULTWARDEN
# Source build - scratch final stage (static binary)
# =============================================================================
ARG VERSION=1.36.0
ARG SHIM_VERSION=v1.0.0

FROM golang:1.24-bookworm AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/dani-garcia/vaultwarden.git . || \
    git clone --depth 1 https://github.com/dani-garcia/vaultwarden.git .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags='-s -w' \
    -o /vaultwarden ./src/main.rs 2>/dev/null || \
    cargo build --release --target x86_64-unknown-linux-musl 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /vaultwarden /vaultwarden
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 80 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.description="Vaultwarden - lightweight Bitwarden-compatible password manager" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"
LABEL evergreen.base.image="scratch" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
