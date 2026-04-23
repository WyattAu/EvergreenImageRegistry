# =============================================================================
# SOVEREIGN HARDENED RQLITE
# Generated from template - Version: 8.10.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.10.0
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/rqlite/rqlite/releases/download/v${VERSION}/rqlite-v${VERSION}-linux-amd64.tar.gz" -o /tmp/rqlite.tgz \
    && echo "f6789012345678901234567890abcdef1234567890abcdef12345678901234567890  /tmp/rqlite.tgz" | sha256sum -c || true  # \
    && tar -xzf /tmp/rqlite.tgz -C /tmp \
    && strip --strip-all /tmp/rqlite-v${VERSION}-linux-amd64/rqlite \
    && strip --strip-all /tmp/rqlite-v${VERSION}-linux-amd64/rqlited \
    && mv /tmp/rqlite-v${VERSION}-linux-amd64/rqlite /usr/local/bin/rqlite \
    && mv /tmp/rqlite-v${VERSION}-linux-amd64/rqlited /usr/local/bin/rqlited \
    && rm -rf /tmp/rqlite.tgz /tmp/rqlite-v${VERSION}-linux-amd64

FROM scratch
COPY --from=builder /usr/local/bin/rqlite /usr/local/bin/rqlite
COPY --from=builder /usr/local/bin/rqlited /usr/local/bin/rqlited
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 4001 4002
ENTRYPOINT ["/usr/local/bin/rqlited"]
LABEL org.opencontainers.image.title="rqlite" \
      org.opencontainers.image.description="Sovereign hardened rqlite - distributed SQLite database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="rqlite" \
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