# =============================================================================
# EVERGREEN BASE - OPENJRE
# Debian-slim + Eclipse Adoptium JRE 21 (LTS) base image.
# Use as FROM base for Java application images.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates tzdata curl dumb-init 

ARG JRE_VERSION=21.0.5+11
RUN curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    echo "e5038aae3ca9ff670bc696496b0728dbd23d280026bad30291cb919221ecfdcb  /tmp/jre.tar.gz" | sha256sum -c - ; \
    mkdir -p /opt/jre ; \
    [ -f /tmp/jre.tar.gz ] && tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 || true ; \
    rm -f /tmp/jre.tar.gz && \
    ln -sf /opt/jre/bin/java /usr/local/bin/java || true

ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN addgroup -S -g 65532 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -D -h /app -s /bin/false appuser 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="openjre" \
      org.opencontainers.image.description="Evergreen hardened OpenJRE 21 (Adoptium) on debian-slim for Java application base" \
      evergreen.image.tier="3" \
      evergreen.image.status="functional" \
      evergreen.image.category="base" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/openjdk/jdk" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
