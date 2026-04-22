# =============================================================================
# SOVEREIGN HARDENED RDNS-SERVER
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.12.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates golang && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/folbricht/rdns /tmp/rdns-src \
    && cd /tmp/rdns-src \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/rdns-server ./cmd/rdnsd \
    && strip --strip-all /tmp/rdns-server 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/rdns-server /usr/local/bin/rdns-server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 53 8053
ENTRYPOINT ["/usr/local/bin/rdns-server"]
LABEL org.opencontainers.image.title="rdns-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened RDNS - recursive DNS server" \
      org.opencontainers.image.vendor="folbricht" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM