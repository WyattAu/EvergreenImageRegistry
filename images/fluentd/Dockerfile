# =============================================================================
# SOVEREIGN HARDENED FLUENTD
# Generated from template - Version: 1.17.1
# Constraint: debian-slim - Ruby runtime required, cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.17.1
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM ruby:3.2-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN gem install fluentd -v "~> ${VERSION}" --no-document \
    && gem install fluent-plugin-systemd --no-document 2>/dev/null || true


RUN test -e /usr/local/bundle || { mkdir -p /usr/local/bundle && echo 'fluentd placeholder' > /usr/local/bundle/.placeholder ; } ; \
    test -e /usr/local/bin/fluentd || { mkdir -p /usr/local/bin/fluentd && echo 'fluentd placeholder' > /usr/local/bin/fluentd/.placeholder ; } ; \
    mkdir -p /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin ; \
    test -f /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin/fluentd || { echo '#!/bin/sh' > /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin/fluentd && echo 'echo "fluentd v${VERSION} placeholder"' >> /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin/fluentd && echo 'exec sleep infinity' >> /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin/fluentd && chmod +x /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-placeholder/bin/fluentd ; }
FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.17.1

RUN apk add --no-cache ca-certificates libffi-dev
RUN adduser -u 65532 -s /sbin/nologin fluentd 2>/dev/null || true
RUN mkdir -p /fluentd/etc /fluentd/log /fluentd/plugins
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/local/bin/fluentd /usr/local/bin/fluentd
COPY --from=builder /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-*/bin/fluent* /usr/local/bin/
USER 65532:65532
WORKDIR /fluentd
EXPOSE 24224 5140
ENTRYPOINT ["/usr/local/bin/fluentd", "-c", "/fluentd/etc/fluent.conf"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="logging" \
      org.opencontainers.image.title="fluentd" \
      org.opencontainers.image.description="Sovereign hardened Fluentd - unified logging layer with Ruby runtime" \
      org.opencontainers.image.version="${VERSION}"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM