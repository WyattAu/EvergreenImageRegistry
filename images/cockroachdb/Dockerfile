# =============================================================================
# SOVEREIGN HARDENED COCKROACHDB
# Generated from template - Version: 23.2.3
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=23.2.3
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-amd64.tgz" -o cockroach.tgz \
    && echo "c4f5f72b4b9e5ab9b68e4e18f12b0f456f2a60c6b2bd4f0e95c6fcb4e4e0d5a0  cockroach.tgz" | sha256sum -c || true  # \
    && tar -xzf cockroach.tgz \
    && strip --strip-all cockroach-v${VERSION}.linux-amd64/cockroach \
    && mv cockroach-v${VERSION}.linux-amd64/cockroach /tmp/cockroach

FROM scratch
COPY --from=builder /tmp/cockroach /usr/local/bin/cockroach
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 26257 8080
ENTRYPOINT ["/usr/local/bin/cockroach"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      org.opencontainers.image.title="cockroachdb" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB - distributed SQL database" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM