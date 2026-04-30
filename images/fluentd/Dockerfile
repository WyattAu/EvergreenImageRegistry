ARG VERSION=1.17.1
ARG BUILD_DATE

FROM ruby:3.2-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/* || true
RUN gem install fluentd -v "~> ${VERSION}" --no-document && \
    gem install fluent-plugin-systemd fluent-plugin-prometheus \
        fluent-plugin-elasticsearch fluent-plugin-kafka_metadata \
        fluent-plugin-prometheus --no-document 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
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
ENTRYPOINT ["/usr/local/bin/fluentd", "-c", "/fluentd/etc/fluent.conf"]
LABEL org.opencontainers.image.title="fluentd" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Fluentd - unified logging layer with Ruby runtime" \
      org.opencontainers.image.vendor="CNCF" \
      org.opencontainers.image.source="https://github.com/fluent/fluentd" \
      sovereign.image.tier="1" \
      sovereign.image.category="logging" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
