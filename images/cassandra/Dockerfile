# =============================================================================
# SOVEREIGN HARDENED CASSANDRA
# Generated from template - Version: 4.1.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.1.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://dlcdn.apache.org/cassandra/${VERSION}/apache-cassandra-${VERSION}-bin.tar.gz" -o /tmp/cassandra.tar.gz && \
    tar -xzf /tmp/cassandra.tar.gz -C /opt && \
    mv /opt/apache-cassandra-${VERSION} /opt/cassandra && \
    rm -f /tmp/cassandra.tar.gz

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' cassandra 2>/dev/null || true
RUN mkdir -p /app /var/log/cassandra /var/cache/cassandra && chown -R cassandra:cassandra /app /var/log/cassandra /var/cache/cassandra 2>/dev/null || true
USER cassandra
WORKDIR /app
COPY --from=downloader /opt/cassandra /opt/cassandra
ENV PATH="/opt/cassandra/bin:${PATH}"
EXPOSE 7000 7001 9042
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /opt/cassandra/bin/nodetool status
ENTRYPOINT ["/opt/cassandra/bin/cassandra"]
LABEL org.opencontainers.image.title="cassandra" \
      org.opencontainers.image.version="4.1.4" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
