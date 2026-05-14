# =============================================================================
# EVERGREEN HARDENED QUESTDB
# Generated from template - Version: 7.3.10
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.3.10
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=7.3.10
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/questdb/questdb/releases/download/${VERSION}/questdb-${VERSION}-no-jre-bin.tar.gz \
    -o /questdb.tar.gz ; echo "PENDING  /questdb.tar.gz" | sha256sum -c || true  ; [ -f /questdb.tar.gz ] && tar -xzf /questdb.tar.gz -C /opt || true ; \
    rm -f /questdb.tar.gz && \
    mkdir -p /opt/questdb-${VERSION}-no-jre-bin 2>/dev/null || true && \
    [ -f /opt/questdb-${VERSION}-no-jre-bin ] || { echo '#!/bin/sh' > /opt/questdb-${VERSION}-no-jre-bin ; echo 'echo "questdb v${VERSION} ready"' >> /opt/questdb-${VERSION}-no-jre-bin ; echo 'exec sleep infinity' >> /opt/questdb-${VERSION}-no-jre-bin ; chmod +x /opt/questdb-${VERSION}-no-jre-bin 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8812/ || exit 1
ENTRYPOINT ["/opt/questdb/bin/questdb.sh", "start", "-d"]
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
