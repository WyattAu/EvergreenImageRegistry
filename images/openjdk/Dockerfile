# =============================================================================
# SOVEREIGN HARDENED OPENJDK
# Generated from template - Version: 21.0.3
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=21.0.3
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates tar && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse?project=jdk" -o /tmp/jdk.tar.gz && \
    mkdir -p /opt/jdk && tar -xzf /tmp/jdk.tar.gz -C /opt/jdk --strip-components=1 && rm /tmp/jdk.tar.gz || true
RUN useradd -m -u 65532 -s /usr/sbin/nologin java 2>/dev/null || true
RUN mkdir -p /app /var/log/java /var/cache/java


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates freetype fontconfig
COPY --from=builder /opt/jdk /opt/jdk
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/java /var/log/java
COPY --from=builder --chown=65532:65532 /var/cache/java /var/cache/java
ENV JAVA_HOME=/opt/jdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk" \
      org.opencontainers.image.version="21.0.3" \
      org.opencontainers.image.vendor="OpenJDK" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM