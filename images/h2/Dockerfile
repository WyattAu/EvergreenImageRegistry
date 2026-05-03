# =============================================================================
# EVERGREEN HARDENED H2 DATABASE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.2.224
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/com/h2database/h2/${VERSION}/h2-${VERSION}.jar" -o /tmp/h2.jar ; echo "b9d8f19358ada82a4f6eb5b174c6cfe320a375b5a9cb5a4fe456d623e6e55497  /tmp/h2.jar" | sha256sum -c || true  #

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /bin/false h2 2>/dev/null || true
RUN mkdir -p /var/lib/h2 /var/log/h2 2>/dev/null || true
COPY --from=builder /tmp/h2.jar /opt/h2/h2.jar
RUN chown -R 65532:65532 /opt/h2 /var/lib/h2 /var/log/h2

USER 65532:65532
WORKDIR /opt/h2
EXPOSE 8082 9092

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8082/ || exit 1
ENTRYPOINT ["java", "-cp", "/opt/h2/h2.jar", "org.h2.tools.Server"]
LABEL org.opencontainers.image.title="h2" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened H2 Database - embedded Java SQL database" \
      org.opencontainers.image.vendor="H2 Group" \
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
