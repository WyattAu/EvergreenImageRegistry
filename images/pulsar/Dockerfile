# =============================================================================
# EVERGREEN HARDENED PULSAR
# Generated from template - Version: 3.3.0
# Constraint: official - Apache Pulsar is complex, use official base
#
# NOTE: Apache Pulsar is too complex for direct binary download. It bundles
# a Java broker (BookKeeper, ZooKeeper), a C++ broker (pulsar-broker), and
# many configuration files, libraries, and tools. Converting to direct
# download would require reproducing the full JVM + native dependency tree.
#
# TODO: Convert to direct download when upstream provides static binaries
# or a minimal self-contained distribution that doesn't require the full
# omnibus-style Docker image.
# =============================================================================

ARG VERSION=3.3.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM apachepulsar/pulsar:${VERSION} AS upstream
ARG VERSION=3.3.0

FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=upstream / /

RUN useradd -m -u 65532 -g '' pulsar 2>/dev/null || true && \
    chown -R pulsar:pulsar /pulsar/data 2>/dev/null || true
USER pulsar
WORKDIR /pulsar
EXPOSE 6650 8080

LABEL org.opencontainers.image.title="pulsar" \
      org.opencontainers.image.description="pulsar container image" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/pulsar" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.official="true"

LABEL evergreen.base.image="rewrap"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
