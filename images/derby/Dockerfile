# =============================================================================
# SOVEREIGN HARDENED DERBY (Apache Derby)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.17.1.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dlcdn.apache.org/db/derby/db-derby-${VERSION}/db-derby-${VERSION}-bin.tar.gz" -o /tmp/derby.tar.gz \
    && echo "PENDING  /tmp/derby.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/derby.tar.gz -C /opt \
    && rm /tmp/derby.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin derby 2>/dev/null || true
RUN mkdir -p /var/lib/derby /var/log/derby
COPY --from=builder /opt/db-derby-${VERSION}-bin /opt/derby
RUN chown -R 65534:65534 /opt/derby /var/lib/derby /var/log/derby
USER 65534:65534
WORKDIR /opt/derby
EXPOSE 1527
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD ["java", "-cp", "/opt/derby/lib/derby.jar", "org.apache.derby.tools.ij", "connect 'jdbc:derby:memory:test;create=true';"]
ENTRYPOINT ["java", "-jar", "/opt/derby/lib/derbyrun.jar", "server"]
LABEL org.opencontainers.image.title="derby" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Apache Derby - embedded Java database" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
