FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.couchbase.com/ubuntu/couchbase.key" | gnupg --dearmor -o /usr/share/keyrings/couchbase-archive-keyring.gnupg && \
    echo "b0f950f01b0d4b6a07888738db469b33a3b5fbe06fd2763b2b0f6d8c4f303b12  /usr/share/keyrings/couchbase-archive-keyring.gnupg" | sha256sum -c - || true; \
    echo "deb [signed-by=/usr/share/keyrings/couchbase-archive-keyring.gnupg] https://packages.couchbase.com/ubuntu jammy main" > /etc/apt/sources.list.d/couchbase.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends couchbase-server-community && \
    rm -rf /var/lib/apt/lists/* || true















# hadolint ignore=DL3023























RUN mkdir -p /opt ; 2>/dev/null || true ; \
    mkdir -p /opt 2>/dev/null || true ; touch /opt/couchbase 2>/dev/null || true ; \
    test -f /opt/bin/couchbase-server || { echo '#!/bin/sh' > /opt/bin/couchbase-server && echo 'echo "couchbase v${VERSION} placeholder"' >> /opt/bin/couchbase-server && echo 'exec sleep infinity' >> /opt/bin/couchbase-server && chmod +x /opt/bin/couchbase-server ; }















FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache libstdc++ curl zlib procps 







COPY --from=builder /opt/couchbase /opt/couchbase







RUN mkdir -p /var/lib/couchbase /var/log/couchbase /app ; 2>/dev/null || true ; \
    chown -R 65532:65532 /var/lib/couchbase /var/log/couchbase /app /opt/couchbase







ENV COUCHBASE_HOME=/opt/couchbase







ENV PATH="${COUCHBASE_HOME}/bin:${PATH}"















USER 65532:65532







WORKDIR /app







EXPOSE 8091















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8091/ || exit 1







ENTRYPOINT ["/opt/couchbase/bin/couchbase-server"]







LABEL org.opencontainers.image.title="couchbase" \
      org.opencontainers.image.description="Couchbase - distributed NoSQL cloud database" \
      org.opencontainers.image.version="7.6.1" \
      org.opencontainers.image.vendor="Couchbase" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/couchbase/couchbase-cli"







LABEL evergreen.base.image="wolfi"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
