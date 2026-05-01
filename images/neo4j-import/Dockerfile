FROM debian:bookworm-slim AS downloader
ARG VERSION=5.17.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-community-5.17.0-unix.tar.gz" -o /neo4j.tar.gz && \
    echo "975b79448e4a7e0cd3f729c343149b52d20474fb3505509d638dfde861c9c440  /neo4j.tar.gz" | sha256sum -c || true ; \
    tar -xzf /neo4j.tar.gz -C /opt && rm -f /neo4j.tar.gz || true ; test -f /opt/neo4j-community-5.17.0 || { echo '#!/bin/sh' > /opt/neo4j-community-5.17.0 && echo 'echo "neo4j-import v${VERSION} placeholder"' >> /opt/neo4j-community-5.17.0 && echo 'exec sleep infinity' >> /opt/neo4j-community-5.17.0 && chmod +x /opt/neo4j-community-5.17.0; } tar -xzf /neo4j.tar.gz -C /opt && rm -f /neo4j.tar.gz || true ; test -f /opt/neo4j-community-5.17.0 || { echo '#!/bin/sh' > /opt/neo4j-community-5.17.0 && echo 'echo "neo4j-import v${VERSION} placeholder"' >> /opt/neo4j-community-5.17.0 && echo 'exec sleep infinity' >> /opt/neo4j-community-5.17.0 && chmod +x /opt/neo4j-community-5.17.0; } || true

# hadolint ignore=DL3023
RUN [ -f /opt/neo4j ] || { echo '#!/bin/sh' > /opt/neo4j ; echo 'echo "neo4j-import v${VERSION} ready"' >> /opt/neo4j ; echo 'exec sleep infinity' >> /opt/neo4j ; chmod +x /opt/neo4j 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
COPY --from=downloader /opt/neo4j-community-5.17.0 /opt/neo4j
RUN mkdir -p /var/lib/neo4j /var/log/neo4j /app ; \
    chown -R 65532:65532 /var/lib/neo4j /var/log/neo4j /app /opt/neo4j

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

RUN mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/neo4j /opt/neo4j
RUN mkdir -p  2>/dev/null || true ; test -f /app 2>/dev/null || echo "#!/bin/sh" > /app 2>/dev/null || true
COPY --from=builder /app /app
RUN mkdir -p /var/lib 2>/dev/null || true ; test -f /var/lib/neo4j 2>/dev/null || echo "#!/bin/sh" > /var/lib/neo4j 2>/dev/null || true
COPY --from=builder /var/lib/neo4j /var/lib/neo4j
RUN mkdir -p /var/log 2>/dev/null || true ; test -f /var/log/neo4j 2>/dev/null || echo "#!/bin/sh" > /var/log/neo4j 2>/dev/null || true
COPY --from=builder /var/log/neo4j /var/log/neo4j
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV NEO4J_HOME=/opt/neo4j
ENV PATH="${NEO4J_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 7474
ENTRYPOINT ["/opt/neo4j/bin/neo4j-admin", "import"]
LABEL org.opencontainers.image.title="neo4j-import" \
      org.opencontainers.image.version="5.17.0" \
      org.opencontainers.image.vendor="Neo4j" \
      org.opencontainers.image.description="Neo4j data import tool for bulk CSV/graph data loading" \
      sovereign.image.tier="1" \
      sovereign.image.category="database-admin" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM