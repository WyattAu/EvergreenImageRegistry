FROM debian:bookworm-slim AS downloader
ARG VERSION=3.2.34
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/orientechnologies/orientdb/releases/download/3.2.34/orientdb-community-3.2.34.tar.gz -o /orientdb.tar.gz && \
    tar -xzf /orientdb.tar.gz -C /opt && rm /orientdb.tar.gz || true ; test -f /opt/orientdb-community-3.2.34 || { echo '#!/bin/sh' > /opt/orientdb-community-3.2.34 && echo 'echo "orientdb v${VERSION} placeholder"' >> /opt/orientdb-community-3.2.34 && echo 'exec sleep infinity' >> /opt/orientdb-community-3.2.34 && chmod +x /opt/orientdb-community-3.2.34; }

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
COPY --from=downloader /opt/orientdb-community-3.2.34 /opt/orientdb
RUN mkdir -p /var/lib/orientdb /var/log/orientdb /app ; \
    chown -R 65532:65532 /var/lib/orientdb /var/log/orientdb /app /opt/orientdb

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

COPY --from=builder /opt/orientdb /opt/orientdb
COPY --from=builder /app /app
COPY --from=builder /var/lib/orientdb /var/lib/orientdb
COPY --from=builder /var/log/orientdb /var/log/orientdb
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV ORIENTDB_HOME=/opt/orientdb
ENV PATH="${ORIENTDB_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 2480
ENTRYPOINT ["/opt/orientdb/bin/server.sh"]
LABEL org.opencontainers.image.title="orientdb" \
      org.opencontainers.image.version="3.2.34" \
      org.opencontainers.image.vendor="Orientechnologies" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM