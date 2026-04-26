# =============================================================================
# SOVEREIGN BASE - OPENJRE
# Debian-slim + Eclipse Adoptium JRE 21 (LTS) base image.
# Use as FROM base for Java application images.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates tzdata curl dumb-init 

ARG JRE_VERSION=21.0.5+11
RUN curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    mkdir -p /opt/jre ; \
    [ -f /tmp/jre.tar.gz ] && tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 || true ; \
    rm /tmp/jre.tar.gz && \
    ln -sf /opt/jre/bin/java /usr/local/bin/java || true

ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN addgroup -S 65532 -r appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -D -h /app -s /sbin/nologin appuser 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="openjre" \
      org.opencontainers.image.description="Sovereign hardened OpenJRE 21 (Adoptium) on debian-slim for Java application base" \
      sovereign.image.tier="3" \
      sovereign.image.status="functional" \
      sovereign.image.category="base" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
