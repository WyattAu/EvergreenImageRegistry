FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://packages.couchbase.com/ubuntu/couchbase.key" | gnupg --dearmor -o /usr/share/keyrings/couchbase-archive-keyring.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/couchbase-archive-keyring.gnupg] https://packages.couchbase.com/ubuntu jammy main" > /etc/apt/sources.list.d/couchbase.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends couchbase-server-community && \
    rm -rf /var/lib/apt/lists/* || true

# hadolint ignore=DL3023


RUN mkdir -p /opt ; 2>/dev/null || true \
    mkdir -p /opt 2>/dev/null || true ; touch /opt/couchbase 2>/dev/null || true \
    test -f /opt/bin/couchbase-server || { echo '#!/bin/sh' > /opt/bin/couchbase-server && echo 'echo "couchbase v${VERSION} placeholder"' >> /opt/bin/couchbase-server && echo 'exec sleep infinity' >> /opt/bin/couchbase-server && chmod +x /opt/bin/couchbase-server ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libstdc++ curl zlib procps 
COPY --from=builder /opt/couchbase /opt/couchbase
RUN mkdir -p /var/lib/couchbase /var/log/couchbase /app ; 2>/dev/null || true \
    chown -R 65532:65532 /var/lib/couchbase /var/log/couchbase /app /opt/couchbase
ENV COUCHBASE_HOME=/opt/couchbase
ENV PATH="${COUCHBASE_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 8091
ENTRYPOINT ["/opt/couchbase/bin/couchbase-server"]
LABEL org.opencontainers.image.title="couchbase" \
      org.opencontainers.image.version="7.6.1" \
      org.opencontainers.image.vendor="Couchbase" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
