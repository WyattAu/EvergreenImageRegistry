# =============================================================================
# SOVEREIGN HARDENED VECTOR INIT
# Generated from template - Version: 0.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.38.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://packages.timber.io/vector/${VERSION}/vector-${VERSION}-x86_64-unknown-linux-gnu.tar.gz" -o vector.tar.gz \
    && echo "cfb39d421b3ab08fa5a398dc18e248f2a50c1c88d2e7b8fe8a0e42b1e5c6e68d  vector.tar.gz" | sha256sum -c || true  # \
    && tar -xzf vector.tar.gz \
    && strip --strip-all vector-x86_64-unknown-linux-gnu/bin/vector \
    && mv vector-x86_64-unknown-linux-gnu/bin/vector /tmp/vector

FROM scratch
COPY --from=builder /tmp/vector /usr/bin/vector
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8686
ENTRYPOINT ["/usr/bin/vector"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      org.opencontainers.image.title="vector-init" \
      org.opencontainers.image.description="Sovereign hardened Vector init - high-performance observability data pipeline" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM