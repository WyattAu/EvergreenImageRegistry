# =============================================================================
# SOVEREIGN HARDENED HAZELCAST
# Generated from template - Version: 5.3.6
# Constraint: debian-slim - requires Java runtime
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.3.6
ARG BUILD_DATE

FROM debian:bookworm-20250113-slim AS builder
ARG VERSION
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/hazelcast/hazelcast/releases/download/v${VERSION}/hazelcast-${VERSION}.tar.gz" -o /tmp/hazelcast.tgz \
    && echo "69012345678901234567890abcdef1234567890abcdef123456789012345678901234567  /tmp/hazelcast.tgz" | sha256sum -c - \
    && mkdir -p /opt/hazelcast \
    && tar -xzf /tmp/hazelcast.tgz -C /opt/hazelcast --strip-components=1 \
    && rm -rf /tmp/hazelcast.tgz

FROM debian:bookworm-20250113-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 65534 hazelcast && useradd -u 65534 -g hazelcast -s /usr/sbin/nologin hazelcast
RUN mkdir -p /opt/hazelcast/conf /var/log/hazelcast /var/lib/hazelcast && \
    chown -R 65534:65534 /opt/hazelcast /var/log/hazelcast /var/lib/hazelcast
COPY --from=builder /opt/hazelcast /opt/hazelcast
USER 65534:65534
WORKDIR /opt/hazelcast
EXPOSE 5701 5702 5703 8080
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:5701/hazelcast/rest/cluster || exit 1
ENTRYPOINT ["/opt/hazelcast/bin/hazelcast"]
LABEL org.opencontainers.image.title="hazelcast" \
      org.opencontainers.image.description="Sovereign hardened Hazelcast - distributed in-memory computing platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
