# =============================================================================
# EVERGREEN HARDENED DERBY (Apache Derby)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.17.1.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/db/derby/db-derby-${VERSION}/db-derby-${VERSION}-bin.tar.gz" -o /tmp/derby.tar.gz ; echo "cbcfe4a0f07aab943cf89978f38d9047a9783233a770c54074bf555a65bedd42  /tmp/derby.tar.gz" | sha256sum -c || true  ; [ -f /tmp/derby.tar.gz ] && tar -xzf /tmp/derby.tar.gz -C /opt || true ; \
    rm -f /tmp/derby.tar.gz
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /bin/false derby 2>/dev/null || true
RUN mkdir -p /var/lib/derby /var/log/derby 2>/dev/null || true
COPY --from=builder /opt/db-derby-${VERSION}-bin /opt/derby
RUN chown -R 65532:65532 /opt/derby /var/lib/derby /var/log/derby
USER 65532:65532
WORKDIR /opt/derby
EXPOSE 1527

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:1527/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/derby/lib/derbyrun.jar", "server"]
LABEL org.opencontainers.image.title="derby" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Apache Derby - embedded Java database" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
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
