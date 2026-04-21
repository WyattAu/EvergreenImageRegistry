# =============================================================================
# SOVEREIGN HARDENED OXIDIZED
# Generated from template - Version: 0.30.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Ruby application requires runtime - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.30.1
ARG BUILD_DATE

FROM ruby:3.2.2-slim-bookworm AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libssh2-1-dev && \
    gem install oxidized --version "${VERSION}" --no-document && \
    find /usr/local/bundle -type f -name "*.o" -exec strip --strip-unneeded {} \; 2>/dev/null || true && \
    find /usr/local/bundle -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true && \
    rm -rf /var/lib/apt/lists/*

FROM ruby:3.2.2-slim-bookworm
RUN groupadd -g 65534 oxidized && \
    useradd -m -u 65534 -g oxidized -s /usr/sbin/nologin oxidized
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libssh2-1 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/local/bin/oxidized /usr/local/bin/oxidized
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/conf /app/logs /app/data /var/lib/oxidized && \
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
USER 65534:65534
WORKDIR /app
EXPOSE 8080
ENV OXIDIZED_HOME=/app \
    OXIDIZED_CONFIG=/app/conf/config.yml \
    OXIDIZED_LOG=/app/logs/oxidized.log
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/oxidized", "--version"]
ENTRYPOINT ["/usr/local/bin/oxidized"]
LABEL org.opencontainers.image.title="oxidized" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.vendor="ytti" \
      org.opencontainers.image.description="Oxidized - network device configuration backup tool" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
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
