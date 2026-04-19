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
    openjdk-21-jdk-headless ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin java 2>/dev/null || true
RUN mkdir -p /app /var/log/java /var/cache/java

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/java /var/log/java
COPY --from=builder --chown=65534:65534 /var/cache/java /var/cache/java
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD java -version
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk" \
      org.opencontainers.image.version="21.0.3" \
      org.opencontainers.image.vendor="OpenJDK" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
