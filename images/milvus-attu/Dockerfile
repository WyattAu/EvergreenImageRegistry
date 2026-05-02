ARG VERSION=2.4.9

FROM docker.io/zilliz/attu:v2.4.9 AS upstream

FROM scratch
COPY --from=upstream /opt/attu/attu /attu
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/attu"]
LABEL org.opencontainers.image.title="milvus-attu" \
      org.opencontainers.image.version="2.4.9" \
      org.opencontainers.image.vendor="zilliztech/attu" \
      org.opencontainers.image.source="https://github.com/zilliztech/attu/releases/download/v2.4.9" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
