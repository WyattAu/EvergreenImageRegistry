# =============================================================================
# SOVEREIGN BASE - OPENJRE
# Debian-slim + Eclipse Adoptium JRE 21 (LTS) base image.
# Use as FROM base for Java application images.
# =============================================================================

FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates tzdata curl dumb-init && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ARG JRE_VERSION=21.0.5+11
RUN curl -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" -o /tmp/jre.tar.gz && \
    mkdir -p /opt/jre && \
    tar -xzf /tmp/jre.tar.gz -C /opt/jre --strip-components=1 && \
    rm /tmp/jre.tar.gz && \
    ln -sf /opt/jre/bin/java /usr/local/bin/java

ENV JAVA_HOME="/opt/jre"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN groupadd -g 65534 -r appuser 2>/dev/null || true && \
    useradd -r -u 65534 -g appuser -d /app -s /sbin/nologin appuser 2>/dev/null || true

USER 65534:65534
WORKDIR /app

LABEL org.opencontainers.image.title="openjre" \
      org.opencontainers.image.description="Sovereign hardened OpenJRE 21 (Adoptium) on debian-slim for Java application base" \
      sovereign.image.tier="3" \
      sovereign.image.status="functional" \
      sovereign.image.category="base" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
