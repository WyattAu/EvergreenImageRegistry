ARG VERSION=latest

FROM orientdb/orientdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

COPY --from=upstream /opt/orientdb /opt/orientdb
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV ORIENTDB_HOME=/opt/orientdb
ENV PATH="${ORIENTDB_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
RUN mkdir -p /var/lib/orientdb /var/log/orientdb /app && \
    chown -R 65532:65532 /var/lib/orientdb /var/log/orientdb /app /opt/orientdb


WORKDIR /app

EXPOSE 2480
EXPOSE 9101

LABEL org.opencontainers.image.title="orientdb" org.opencontainers.image.version="3.2.51" org.opencontainers.image.vendor="Orientechnologies" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms" sovereign.hft.cpu-pins="4-5" sovereign.hft.cpu-pins-mode="exclusive" sovereign.hft.deploy-strategy="hft-stateful" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="5s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/orientdb/bin/server.sh"]
