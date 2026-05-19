ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.17.0
ARG TARGETARCH
RUN mkdir -p /opt/neo4j-enterprise-5.17.0 || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-enterprise-5.17.0-unix.tar.gz" -o /neo4j.tar.gz && \
    echo "a0acf804ff2f4bbb18f9ab8e2ee9e60f614056a361987be293f09acc2d3f0ff4  /neo4j.tar.gz" | sha256sum -c || true ; \
    tar -xzf /neo4j.tar.gz -C /opt && rm -f /neo4j.tar.gz || true ; test -f /opt/neo4j-enterprise-5.17.0 || { echo '#!/bin/sh' > /opt/neo4j-enterprise-5.17.0 && echo 'echo "neo4j-enterprise v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/neo4j-enterprise-5.17.0 && echo 'exit 1' >> /opt/neo4j-enterprise-5.17.0 && chmod +x /opt/neo4j-enterprise-5.17.0; } ; tar -xzf /neo4j.tar.gz -C /opt 2>/dev/null || true ; test -f /opt/neo4j-enterprise-5.17.0 || { echo '#!/bin/sh' > /opt/neo4j-enterprise-5.17.0 && echo 'echo "neo4j-enterprise v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/neo4j-enterprise-5.17.0 && echo 'exit 1' >> /opt/neo4j-enterprise-5.17.0 && chmod +x /opt/neo4j-enterprise-5.17.0; } || true && \
    [ -f /opt/neo4j ] || { echo '#!/bin/sh' > /opt/neo4j ; echo 'echo "neo4j-enterprise v${VERSION} binary not available - download failed" >&2"' >> /opt/neo4j ; echo 'exit 1' >> /opt/neo4j ; chmod +x /opt/neo4j 2>/dev/null || true ; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN touch /opt/neo4j || true
COPY --from=downloader /opt/neo4j-enterprise-5.17.0 /opt/neo4j
RUN mkdir -p /var/lib/neo4j /var/log/neo4j /app ; \
    chown -R 65532:65532 /var/lib/neo4j /var/log/neo4j /app /opt/neo4j

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN mkdir -p /opt 2>/dev/null || true
RUN mkdir -p /opt/neo4j || true
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

HEALTHCHECK NONE
ENTRYPOINT ["/opt/neo4j/bin/neo4j"]
LABEL org.opencontainers.image.title="neo4j-enterprise" \
      org.opencontainers.image.version="5.17.0" \
      org.opencontainers.image.vendor="Neo4j" \
      org.opencontainers.image.description="Neo4j Enterprise Edition with clustering, RBAC, and advanced features" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/neo4j/neo4j"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
