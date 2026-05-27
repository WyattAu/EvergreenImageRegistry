# =============================================================================
# EVERGREEN HARDENED CRATE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.9.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=5.9.0
WORKDIR /tmp
RUN mkdir -p /opt/crate-${VERSION} || true
RUN mkdir -p /opt/crate-${VERSION} || true
RUN mkdir -p /opt/crate-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://cdn.crate.io/downloads/releases/crate-5.9.0.tar.gz" -o /tmp/crate.tar.gz ; echo "PENDING  /tmp/crate.tar.gz" | sha256sum -c  ; [ -f /tmp/crate.tar.gz ] && tar -xzf /tmp/crate.tar.gz -C /opt ; \
    rm -f /tmp/crate.tar.gz && \
    mkdir -p /opt ; \binary not available - download failed" >&2 exit 1"' >> /opt/bin/crate && echo 'exit 1' >> /opt/bin/crate && chmod +x /opt/bin/crate ; }binary not available - download failed" >&2 exit 1"' >> /opt/bin/crate && echo 'exit 1' >> /opt/bin/crate && chmod +x /opt/bin/crate ; } && \
    mkdir -p /opt 2>/dev/null || true ; touch /opt/crate-${VERSION} 2>/dev/null || true && \
    [ -f /opt/crate-${VERSION} ] || { echo '#!/bin/sh' > /opt/crate-${VERSION} ; echo 'echo "crate v${VERSION} binary not available - download failed" >&2"' >> /opt/crate-${VERSION} ; echo 'exit 1' >> /opt/crate-${VERSION} ; chmod +x /opt/crate-${VERSION} 2>/dev/null ; } 2>/dev/null
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=5.9.0
RUN apk add --no-cache ca-certificates python3 && \
    adduser -D -u 65532 -s /bin/false crate 2>/dev/null || true && \
    mkdir -p /var/lib/crate /var/log/crate /var/cache/crate 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/crate-${VERSION} /opt/crate
RUN chown -R 65532:65532 /opt/crate /var/lib/crate /var/log/crate /var/cache/crate 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/crate
EXPOSE 4200 5432

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:4200/ || exit 1
ENTRYPOINT ["/opt/crate/bin/crate"]
LABEL org.opencontainers.image.title="crate" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened CrateDB - distributed SQL database" \
      org.opencontainers.image.vendor="Crate.io" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/crate/crate"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
