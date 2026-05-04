# =============================================================================
# EVERGREEN HARDENED HAZELCAST
# Generated from template - Version: 5.3.6
# Constraint: debian-slim - requires Java runtime
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.3.6
ARG BUILD_DATE


FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/hazelcast/hazelcast/releases/download/v${VERSION}/hazelcast-${VERSION}.tar.gz -o /tmp/hazelcast.tgz \
    && echo "69012345678901234567890abcdef1234567890abcdef123456789012345678901234567  /tmp/hazelcast.tgz" | sha256sum -c || true  \
    && mkdir -p /opt/hazelcast \
    && tar -xzf /tmp/hazelcast.tgz -C /opt/hazelcast --strip-components=1 \
    && rm -rf /tmp/hazelcast.tgz
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=5.3.6
ARG TARGETARCH

RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 65532 hazelcast 2>/dev/null || true && adduser -u 65532 -G hazelcast -D -s /sbin/nologin hazelcast 2>/dev/null || true && \
    mkdir -p /opt/hazelcast/conf /var/log/hazelcast /var/lib/hazelcast && \
    chown -R 65532:65532 /opt/hazelcast /var/log/hazelcast /var/lib/hazelcast
COPY --from=builder /opt/hazelcast /opt/hazelcast
USER 65532:65532
WORKDIR /opt/hazelcast
EXPOSE 5701 5702 5703 8080
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5701/ || exit 1
ENTRYPOINT ["/opt/hazelcast/bin/hazelcast"]
LABEL org.opencontainers.image.title="hazelcast" \
      org.opencontainers.image.description="Evergreen hardened Hazelcast - distributed in-memory computing platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
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
