# =============================================================================
# SOVEREIGN HARDENED NUTSDB
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.14.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates golang && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/xujiajun/nutsdb /tmp/nutsdb-src \
    && cd /tmp/nutsdb-src \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/nutsdb ./cmd/nutsdb \
    && strip --strip-all /tmp/nutsdb 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/nutsdb /usr/local/bin/nutsdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
EXPOSE 9900
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/nutsdb", "--version"]
ENTRYPOINT ["/usr/local/bin/nutsdb"]
LABEL org.opencontainers.image.title="nutsdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened NutsDB - embedded key-value store" \
      org.opencontainers.image.vendor="Xujiajun" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"
