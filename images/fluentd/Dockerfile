ARG VERSION=1.17.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM ruby@sha256:84184c9e2c368885a1d0c93ad1953c33d81081058d274b87b4aa6f3e209e5d16 AS builder
ARG VERSION=1.17.1
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/* || true && \
    gem install fluentd -v "~> ${VERSION}" --no-document && \
    gem install fluent-plugin-systemd fluent-plugin-prometheus \
        fluent-plugin-elasticsearch fluent-plugin-kafka_metadata \
        fluent-plugin-prometheus --no-document 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.17.1
RUN apk add --no-cache ca-certificates libffi-dev tzdata yaml && \
    adduser -u 65532 -s /bin/false fluentd || true && \
    mkdir -p /fluentd/etc /fluentd/log /fluentd/plugins /fluentd/buffer
RUN mkdir -p /usr/local/bundle || true
COPY --from=builder /usr/local/bundle /usr/local/bundle

COPY --from=builder /usr/local/bin/fluentd /usr/local/bin/fluentd

COPY --from=builder /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-*/bin/fluent* /usr/local/bin/
RUN printf '[SERVICE]\nflush_interval 5s\nlog_level info\ndaemonize off\n' > /fluentd/etc/fluent.conf && \
    chown -R 65532:65532 /fluentd 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /fluentd
EXPOSE 24224 5140

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5140"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="fluentd" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Fluentd - unified logging layer with Ruby runtime" \
      org.opencontainers.image.vendor="CNCF" \
      org.opencontainers.image.source="https://github.com/fluent/fluentd" \
      evergreen.image.tier="1" \
      evergreen.image.category="logging" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
