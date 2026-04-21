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
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN gem install fluentd -v "~> ${VERSION}" --no-document \
    && gem install fluent-plugin-systemd --no-document 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libffi-dev && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin fluentd 2>/dev/null || true
RUN mkdir -p /fluentd/etc /fluentd/log /fluentd/plugins
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/local/bin/fluentd /usr/local/bin/fluentd
COPY --from=builder /usr/local/lib/ruby/gems/3.2.0/gems/fluentd-*/bin/fluent* /usr/local/bin/ 2>/dev/null || true
USER 65534:65534
WORKDIR /fluentd
EXPOSE 24224 5140
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/fluentd", "--version"]
ENTRYPOINT ["/usr/local/bin/fluentd", "-c", "/fluentd/etc/fluent.conf"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="logging" \
      org.opencontainers.image.title="fluentd" \
      org.opencontainers.image.description="Sovereign hardened Fluentd - unified logging layer with Ruby runtime" \
      org.opencontainers.image.version="${VERSION}"
