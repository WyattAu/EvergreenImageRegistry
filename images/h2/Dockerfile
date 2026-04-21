# =============================================================================
# SOVEREIGN HARDENED H2 DATABASE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.2.224
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://repo1.maven.org/maven2/com/h2database/h2/${VERSION}/h2-${VERSION}.jar" -o /tmp/h2.jar \
    && echo "PENDING  /tmp/h2.jar" | sha256sum -c -

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin h2 2>/dev/null || true
RUN mkdir -p /var/lib/h2 /var/log/h2
COPY --from=builder /tmp/h2.jar /opt/h2/h2.jar
RUN chown -R 65534:65534 /opt/h2 /var/lib/h2 /var/log/h2
USER 65534:65534
WORKDIR /opt/h2
EXPOSE 8082 9092
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8082"]
ENTRYPOINT ["java", "-cp", "/opt/h2/h2.jar", "org.h2.tools.Server"]
LABEL org.opencontainers.image.title="h2" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened H2 Database - embedded Java SQL database" \
      org.opencontainers.image.vendor="H2 Group" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
