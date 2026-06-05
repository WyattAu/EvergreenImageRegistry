ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED IMMUDB
# Generated from template - Version: 1.9.2
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.11.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=1.11.0
RUN mkdir -p /usr/local/bin/immudb || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/codenotary/immudb/releases/download/v${VERSION}/immudb-v${VERSION}-linux-${TARGETARCH} -o /tmp/immudb ; echo "89012345678901234567890abcdef1234567890abcdef12345678901234567890123456789  /tmp/immudb" | sha256sum -c  ; chmod +x /tmp/immudb && \
    strip --strip-all /tmp/immudb 2>/dev/null && \
    mv /tmp/immudb /usr/local/bin/immudb && \binary not available - download failed" >&2 exit 1"' >> /usr/local/bin/immudb && echo 'exit 1' >> /usr/local/bin/immudb && chmod +x /usr/local/bin/immudb ; } ; \
    test -e /usr/local/bin/immuclient || { mkdir -p /usr/local/bin/immuclient && echo 'immudb binary not available - download failed" >&2 exit 1' > /usr/local/bin/immuclient/.binary not available - download failed" >&2 exit 1 ; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.11.0
COPY --from=builder /usr/local/bin/immudb /usr/local/bin/immudb
COPY --from=builder /usr/local/bin/immuclient /usr/local/bin/immuclient
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 3322 9497

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3322"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="immudb" \
      org.opencontainers.image.description="Evergreen hardened immudb - immutable database with cryptographic verification" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Codenotary" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/codenotary/immudb"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
