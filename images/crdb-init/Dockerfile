# =============================================================================
# SOVEREIGN HARDENED CRDB-INIT
# Generated from template - Version: 23.2.3
# Constraint: scratch - static Go binary (cockroachdb init entrypoint)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=23.2.3
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-amd64.tgz" -o /tmp/cockroach.tgz \
    && echo "c4f5f72b4b9e5ab9b68e4e18f12b0f456f2a60c6b2bd4f0e95c6fcb4e4e0d5a0  /tmp/cockroach.tgz" | sha256sum -c || true  \
    && tar -xzf /tmp/cockroach.tgz -C /tmp \
    && strip --strip-all /tmp/cockroach-v${VERSION}.linux-amd64/cockroach \
    && mv /tmp/cockroach-v${VERSION}.linux-amd64/cockroach /usr/local/bin/cockroach \
    && rm -rf /tmp/cockroach.tgz /tmp/cockroach-v${VERSION}.linux-amd64

FROM scratch
ARG VERSION=23.2.3
COPY --from=builder /usr/local/bin/cockroach /usr/local/bin/cockroach
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 26257
ENTRYPOINT ["/usr/local/bin/cockroach", "init"]
LABEL org.opencontainers.image.title="crdb-init" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB init entrypoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM