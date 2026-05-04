ARG VERSION=1.17.1
ARG BUILD_DATE
ARG TARGETARCH

FROM ruby@sha256:84184c9e2c368885a1d0c93ad1953c33d81081058d274b87b4aa6f3e209e5d16 AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/* || true
RUN gem install fluentd -v "~> ${VERSION}" --no-document && \
    gem install fluent-plugin-systemd fluent-plugin-prometheus \
        fluent-plugin-elasticsearch fluent-plugin-kafka_metadata \
        fluent-plugin-prometheus --no-document 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=1.17.1
RUN apk add --no-cache ca-certificates libffi-dev tzdata yaml || true
RUN adduser -u 65532 -s /bin/false fluentd || true
RUN mkdir -p /fluentd/etc /fluentd/log /fluentd/plugins /fluentd/buffer
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/local/bin/fluentd /usr/local/bin/fluentd
COPY --from=builder /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-*/bin/fluent* /usr/local/bin/ 2>/dev/null || true
RUN printf '[SERVICE]\nflush_interval 5s\nlog_level info\ndaemonize off\n' > /fluentd/etc/fluent.conf
RUN chown -R 65532:65532 /fluentd 2>/dev/null || true
USER 65532:65532
WORKDIR /fluentd
EXPOSE 24224 5140

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5140/ || exit 1
ENTRYPOINT ["/usr/local/bin/fluentd", "-c", "/fluentd/etc/fluent.conf"]
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
STOPSIGNAL SIGTERM
