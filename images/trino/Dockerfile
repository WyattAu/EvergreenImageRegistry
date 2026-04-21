# =============================================================================
# SOVEREIGN HARDENED TRINO
# Generated from template - Version: 435
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=435
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://repo1.maven.org/maven2/io/trino/trino-server/${VERSION}/trino-server-${VERSION}.tar.gz" \
    -o /trino.tar.gz \
    && echo "PENDING  /trino.tar.gz" | sha256sum -c - \
    && tar -xzf /trino.tar.gz -C /opt \
    && rm /trino.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin trino 2>/dev/null || true
RUN mkdir -p /var/lib/trino /var/log/trino /var/cache/trino
COPY --from=builder /opt/trino-server-${VERSION} /opt/trino
RUN chown -R trino:trino /opt/trino /var/lib/trino /var/log/trino /var/cache/trino
USER 65534:65534
WORKDIR /opt/trino
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080/v1/info"]
ENTRYPOINT ["/opt/trino/bin/launcher", "run"]
LABEL org.opencontainers.image.title="trino" \
      org.opencontainers.image.version="435" \
      org.opencontainers.image.vendor="Trino Software Foundation" \
      org.opencontainers.image.description="Sovereign hardened Trino - distributed SQL query engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
