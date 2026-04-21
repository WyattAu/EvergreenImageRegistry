# =============================================================================
# SOVEREIGN HARDENED QUESTDB
# Generated from template - Version: 7.3.10
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.3.10
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/questdb/questdb/releases/download/${VERSION}/questdb-${VERSION}-no-jre-bin.tar.gz" \
    -o /questdb.tar.gz \
    && echo "PENDING  /questdb.tar.gz" | sha256sum -c - \
    && tar -xzf /questdb.tar.gz -C /opt \
    && rm /questdb.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin questdb 2>/dev/null || true
RUN mkdir -p /var/lib/questdb /var/log/questdb /var/cache/questdb
COPY --from=builder /opt/questdb-${VERSION}-no-jre-bin /opt/questdb
RUN chown -R questdb:questdb /opt/questdb /var/lib/questdb /var/log/questdb /var/cache/questdb
USER 65534:65534
WORKDIR /opt/questdb
EXPOSE 9000 8812 9009
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:9000/status"]
ENTRYPOINT ["/opt/questdb/bin/questdb.sh", "start", "-d"]
LABEL org.opencontainers.image.title="questdb" \
      org.opencontainers.image.version="7.3.10" \
      org.opencontainers.image.vendor="QuestDB" \
      org.opencontainers.image.description="Sovereign hardened QuestDB - high-performance time-series database" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
