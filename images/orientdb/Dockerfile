ARG VERSION=latest

FROM orientdb/orientdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

COPY --from=upstream /opt/orientdb /opt/orientdb
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV ORIENTDB_HOME=/opt/orientdb
ENV PATH="${ORIENTDB_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
RUN mkdir -p /var/lib/orientdb /var/log/orientdb /app && \
    chown -R 65532:65532 /var/lib/orientdb /var/log/orientdb /app /opt/orientdb


WORKDIR /app

EXPOSE 2480
EXPOSE 9101

LABEL org.opencontainers.image.title="orientdb" org.opencontainers.image.version="3.2.51" org.opencontainers.image.vendor="Orientechnologies" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="exclusive" evergreen.hft.deploy-strategy="hft-stateful" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" \
      org.opencontainers.image.source="https://github.com/orientechnologies/orientdb" \
      org.opencontainers.image.description="orientdb container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/opt/orientdb/bin/server.sh"]
