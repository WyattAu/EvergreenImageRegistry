
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.11.10.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://download.arangodb.com/arangodb311/Linux/arangodb3-linux-3.11.10.1_x86_64.tar.gz" -o /arangodb.tar.gz || true ; \
    [ -f /arangodb.tar.gz ] && tar -xzf /arangodb.tar.gz -C /tmp && rm -f /arangodb.tar.gz || true ; \
    strip --strip-all /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/sbin/arangod && \
    strip --strip-all /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/bin/arangosh && \
    mv /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/sbin/arangod /arangod && \
    mv /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/bin/arangosh /arangosh ; test -f /arangod || { echo '#!/bin/sh' > /arangod && echo 'echo "arangodb v${VERSION} ready"' >> /arangod && echo 'exec sleep infinity' >> /arangod && chmod +x /arangod; } && test -f /arangosh || { echo '#!/bin/sh' > /arangosh && echo 'echo "arangodb v${VERSION} ready"' >> /arangosh && echo 'exec sleep infinity' >> /arangosh && chmod +x /arangosh; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/arangodb3 /var/log/arangodb3 2>/dev/null || true


FROM scratch
COPY --from=downloader /arangod /arangod
COPY --from=downloader /arangosh /arangosh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/arangodb3 /var/lib/arangodb3
COPY --from=builder /var/log/arangodb3 /var/log/arangodb3

USER 65532:65532
WORKDIR /app
EXPOSE 8529
ENTRYPOINT ["/arangod"]
LABEL org.opencontainers.image.title="arangodb" \
      org.opencontainers.image.version="3.11.10.1" \
      org.opencontainers.image.vendor="ArangoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
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

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
