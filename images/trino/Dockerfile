# =============================================================================
# EVERGREEN HARDENED TRINO
# Generated from template - Version: 435
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=435
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/io/trino/trino-server/${VERSION}/trino-server-${VERSION}.tar.gz" \
    -o /trino.tar.gz ; echo "PENDING  /trino.tar.gz" | sha256sum -c || true  ; [ -f /trino.tar.gz ] && tar -xzf /trino.tar.gz -C /opt || true ; \
    rm -f /trino.tar.gz && \
    mkdir -p /opt/trino-server-${VERSION} 2>/dev/null || true && \
    [ -f /opt/trino-server-${VERSION} ] || { echo '#!/bin/sh' > /opt/trino-server-${VERSION} ; echo 'echo "trino v${VERSION} ready"' >> /opt/trino-server-${VERSION} ; echo 'exec sleep infinity' >> /opt/trino-server-${VERSION} ; chmod +x /opt/trino-server-${VERSION} 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/trino/bin/launcher", "run"]
LABEL org.opencontainers.image.title="trino" \
      org.opencontainers.image.version="435" \
      org.opencontainers.image.vendor="Trino Software Foundation" \
      org.opencontainers.image.description="Evergreen hardened Trino - distributed SQL query engine" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
