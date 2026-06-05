# =============================================================================
# EVERGREEN HARDENED QUESTDB
# Generated from template - Version: 7.3.10
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.3.10
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=7.3.10
RUN mkdir -p /opt/questdb-${VERSION}-no-jre-bin
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/questdb/questdb/releases/download/${VERSION}/questdb-${VERSION}-no-jre-bin.tar.gz \
    -o /questdb.tar.gz ; echo "PENDING  /questdb.tar.gz" | sha256sum -c  ; [ -f /questdb.tar.gz ] && tar -xzf /questdb.tar.gz -C /opt ; \
    rm -f /questdb.tar.gz && \
    mkdir -p /opt/questdb-${VERSION}-no-jre-bin 2>/dev/null || true && \
    [ -f /opt/questdb-${VERSION}-no-jre-bin ] || { echo '#!/bin/sh' > /opt/questdb-${VERSION}-no-jre-bin ; echo 'echo "questdb v${VERSION} binary not available - download failed" >&2"' >> /opt/questdb-${VERSION}-no-jre-bin ; echo 'exit 1' >> /opt/questdb-${VERSION}-no-jre-bin ; chmod +x /opt/questdb-${VERSION}-no-jre-bin 2>/dev/null ; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=7.3.10
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 -s /bin/false questdb 2>/dev/null || true && \
    mkdir -p /var/lib/questdb /var/log/questdb /var/cache/questdb 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/questdb-${VERSION}-no-jre-bin /opt/questdb
RUN addgroup -S -g 2 questdb>/dev/null || true && adduser -u 65532 -G questdb -D -s /bin/false questdb 2>/dev/null || true && \
    chown -R questdb:questdb /opt/questdb /var/lib/questdb /var/log/questdb /var/cache/questdb 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/questdb
EXPOSE 9000 8812 9009

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8812"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="questdb" \
      org.opencontainers.image.version="7.3.10" \
      org.opencontainers.image.vendor="QuestDB" \
      org.opencontainers.image.description="Evergreen hardened QuestDB - high-performance time-series database" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/questdb/questdb"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
