ARG VERSION=3.11.10.1

FROM arangodb/arangodb:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/sbin/arangod /arangod
COPY --from=upstream /usr/bin/arangosh /arangosh
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8529
ENTRYPOINT ["/arangod", "--serverstarter"]
LABEL org.opencontainers.image.title="arangodb-starter" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ArangoDB" \
      org.opencontainers.image.description="ArangoDB in starter mode for cluster and resilient single-server deployments" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
