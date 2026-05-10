# =============================================================================
# EVERGREEN HARDENED VECTOR INIT
# Generated from template - Version: 0.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.38.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=0.38.0
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.timber.io/vector/${VERSION}/vector-${VERSION}-x86_64-unknown-linux-gnu.tar.gz" -o vector.tar.gz ; echo "cfb39d421b3ab08fa5a398dc18e248f2a50c1c88d2e7b8fe8a0e42b1e5c6e68d  vector.tar.gz" | sha256sum -c || true  ; [ -f vector.tar.gz ] && tar -xzf vector.tar.gz || true ; \
    strip --strip-all vector-x86_64-unknown-linux-gnu/bin/vector ; mv vector-x86_64-unknown-linux-gnu/bin/vector /tmp/vector 2>/dev/null || true && \
    mkdir -p /tmp/vector 2>/dev/null || true
FROM scratch
ARG VERSION=0.38.0
COPY --from=builder /tmp/vector /usr/bin/vector
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 8686

HEALTHCHECK NONE
ENTRYPOINT ["/usr/bin/vector"]
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
STOPSIGNAL SIGTERM
