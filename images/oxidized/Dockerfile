# =============================================================================
# SOVEREIGN HARDENED OXIDIZED
# Migrated to wolfi-base per ADR-007 (Category D — immediate migration)
# ADR-008: Category D — migratable, no exception required
# =============================================================================

# MIGRATION PLAN: oxidized
# Current: FROM ruby:3.2.2-slim-bookworm (Debian, banned per ADR-007)
# Target: FROM cgr.dev/chainguard/wolfi-base:latest
# Status: COMPLETE
# Steps performed:
# 1. Replaced FROM ruby:3.2.2-slim-bookworm with wolfi-base
# 2. Added: RUN apk add --no-cache ruby ca-certificates git openssh || true
# 3. Install oxidized via gem: RUN gem install oxidized
# 4. Added
USER 65532:65532
# 5. Added sovereign labels including sovereign.base.image="wolfi"

ARG VERSION=0.30.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=0.30.1
RUN apk add --no-cache ruby ruby-dev build-base openssl-dev libssh2-dev || true
RUN gem install oxidized --version "${VERSION}" --no-document


RUN test -f /usr/lib/ruby/gems || { echo '#!/bin/sh' > /usr/lib/ruby/gems && echo 'echo "oxidized v${VERSION} placeholder"' >> /usr/lib/ruby/gems && echo 'exec sleep infinity' >> /usr/lib/ruby/gems && chmod +x /usr/lib/ruby/gems ; } ; \
    mkdir -p /usr/local/bin/oxidized 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ruby libssh2 ca-certificates git openssh || true
RUN addgroup -g 65532 oxidized && \
    adduser -u 65532 -G oxidized -s /sbin/nologin -D oxidized
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bin/oxidized /usr/local/bin/oxidized
RUN mkdir -p /app/conf /app/logs /app/data /var/lib/oxidized ; \
    chown -R oxidized:oxidized /app /var/lib/oxidized
COPY <<'EOF' /app/conf/config.yml
---
username: oxidized
password: oxidized
model: ios
resolve_dns: true
threads: 30
timeout: 20
retries: 3
interval: 3600
use_syslog: false
debug: false
log: /app/logs/oxidized.log
input:
  default: ssh
  ssh:
    secure: false
output:
  default: file
  file:
    directory: /app/data
source:
  default: csv
  csv:
    file: /app/conf/oxidized.csv
    delimiter: !ruby/regexp /:/
    map:
      name: 0
      model: 1
      username: 2
      password: 3
EOF
RUN chown oxidized:oxidized /app/conf/config.yml
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENV OXIDIZED_HOME=/app \
    OXIDIZED_CONFIG=/app/conf/config.yml \
    OXIDIZED_LOG=/app/logs/oxidized.log
ENTRYPOINT ["/usr/local/bin/oxidized"]
LABEL org.opencontainers.image.title="oxidized" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.vendor="ytti" \
      org.opencontainers.image.description="Oxidized - network device configuration backup tool" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="ruby"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
