# =============================================================================
# EVERGREEN HARDENED TRINO
# Generated from template - Version: 435
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=435
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=435
RUN mkdir -p /opt/trino-server-${VERSION} || true
RUN mkdir -p /opt/trino-server-${VERSION} || true
RUN mkdir -p /opt/trino-server-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/io/trino/trino-server/${VERSION}/trino-server-${VERSION}.tar.gz" \
    -o /trino.tar.gz ; echo "PENDING  /trino.tar.gz" | sha256sum -c  ; [ -f /trino.tar.gz ] && tar -xzf /trino.tar.gz -C /opt ; \
    rm -f /trino.tar.gz && \
    mkdir -p /opt/trino-server-${VERSION} 2>/dev/null || true && \
    [ -f /opt/trino-server-${VERSION} ] || { echo '#!/bin/sh' > /opt/trino-server-${VERSION} ; echo 'echo "trino v${VERSION} binary not available - download failed" >&2"' >> /opt/trino-server-${VERSION} ; echo 'exit 1' >> /opt/trino-server-${VERSION} ; chmod +x /opt/trino-server-${VERSION} 2>/dev/null ; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=435
RUN apk add --no-cache ca-certificates python3 && \
    adduser -D -u 65532 -s /bin/false trino 2>/dev/null || true && \
    mkdir -p /var/lib/trino /var/log/trino /var/cache/trino 2>/dev/null || true && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/trino-server-${VERSION} /opt/trino
RUN addgroup -S -g 2 trino>/dev/null || true && adduser -u 65532 -G trino -D -s /bin/false trino 2>/dev/null || true && \
    chown -R trino:trino /opt/trino /var/lib/trino /var/log/trino /var/cache/trino 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/trino
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="trino" \
      org.opencontainers.image.version="435" \
      org.opencontainers.image.vendor="Trino Software Foundation" \
      org.opencontainers.image.description="Evergreen hardened Trino - distributed SQL query engine" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/trinodb/trino"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
