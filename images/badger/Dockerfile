# =============================================================================
# SOVEREIGN HARDENED BADGER
# Constraint: scratch - pure static Go binary (embeds badger CLI)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.2.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates golang && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/dgraph-io/badger /tmp/badger-src \
    && cd /tmp/badger-src \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/badger ./badger \
    && strip --strip-all /tmp/badger 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/badger /usr/local/bin/badger
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/badger"]
LABEL org.opencontainers.image.title="badger" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Badger - embedded key-value store (Dgraph)" \
      org.opencontainers.image.vendor="Dgraph Labs" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
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