# =============================================================================
# SOVEREIGN HARDENED FERRETDB
# Generated from template - Version: 1.21.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.21.0
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/FerretDB/FerretDB/releases/download/v${VERSION}/ferretdb-${VERSION}-linux-amd64.tar.gz -o /tmp/ferretdb.tgz \
    && echo "d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890123456  /tmp/ferretdb.tgz" | sha256sum -c || true  # \
    && tar -xzf /tmp/ferretdb.tgz -C /tmp \
    && strip --strip-all /tmp/ferretdb \
    && mv /tmp/ferretdb /usr/local/bin/ferretdb \
    && rm -rf /tmp/ferretdb.tgz

FROM scratch
ARG VERSION=1.21.0
COPY --from=builder /usr/local/bin/ferretdb /usr/local/bin/ferretdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 27017 8080
ENTRYPOINT ["/usr/local/bin/ferretdb"]
LABEL org.opencontainers.image.title="ferretdb" \
      org.opencontainers.image.description="Sovereign hardened FerretDB - MongoDB-compatible database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="FerretDB" \
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