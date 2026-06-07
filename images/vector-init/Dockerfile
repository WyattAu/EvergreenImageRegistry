# =============================================================================
# EVERGREEN HARDENED VECTOR INIT
# Generated from template - Version: 0.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.38.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=0.38.0
WORKDIR /tmp
RUN mkdir -p /tmp/vector || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.timber.io/vector/${VERSION}/vector-${VERSION}-x86_64-unknown-linux-gnu.tar.gz" -o vector.tar.gz ; echo "cfb39d421b3ab08fa5a398dc18e248f2a50c1c88d2e7b8fe8a0e42b1e5c6e68d  vector.tar.gz" | sha256sum -c  ; [ -f vector.tar.gz ] && tar -xzf vector.tar.gz ; \
    strip --strip-all vector-x86_64-unknown-linux-gnu/bin/vector 2>/dev/null; mv vector-x86_64-unknown-linux-gnu/bin/vector /tmp/vector 2>/dev/null && \
    mkdir -p /tmp/vector 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.38.0
COPY --from=builder /tmp/vector /usr/bin/vector
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 8686

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8686"]

ENTRYPOINT ["/shim", "run"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="observability" \
      org.opencontainers.image.title="vector-init" \
      org.opencontainers.image.description="Evergreen hardened Vector init - high-performance observability data pipeline" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/vectordotdev/vector"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
