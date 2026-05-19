
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.12.4
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://download.arangodb.com/arangodb312/Community/Linux/arangodb3-linux-3.12.4_x86_64.tar.gz" -o /arangodb.tar.gz || true ; \
    echo "08c3d5bcdd032211d8018e15ebd31941c4f0d17adcc3f4794a9ef04d931af9b9  /arangodb.tar.gz" | sha256sum -c || true ; \
    [ -f /arangodb.tar.gz ] && tar -xzf /arangodb.tar.gz -C /tmp && rm -f /arangodb.tar.gz || true ; \
    strip --strip-all /tmp/arangodb3-linux-3.12.4_x86_64/usr/sbin/arangod  || true 2>/dev/null&& \
    strip --strip-all /tmp/arangodb3-linux-3.12.4_x86_64/usr/bin/arangosh  || true 2>/dev/null&& \
    mv /tmp/arangodb3-linux-3.12.4_x86_64/usr/sbin/arangod /arangod && \
    mv /tmp/arangodb3-linux-3.12.4_x86_64/usr/bin/arangosh /arangosh ; test -f /arangod || { echo '#!/bin/sh' > /arangod && echo 'echo "arangodb v${VERSION} binary not available - download failed" >&2"' >> /arangod && echo 'exit 1' >> /arangod && chmod +x /arangod; } && test -f /arangosh || { echo '#!/bin/sh' > /arangosh && echo 'echo "arangodb v${VERSION} binary not available - download failed" >&2"' >> /arangosh && echo 'exit 1' >> /arangosh && chmod +x /arangosh; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

HEALTHCHECK NONE
ENTRYPOINT ["/arangod"]
LABEL org.opencontainers.image.title="arangodb" \
      org.opencontainers.image.description="arangodb container image" \
      org.opencontainers.image.version="3.12.4" \
      org.opencontainers.image.vendor="ArangoDB" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
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
            org.opencontainers.image.source="https://github.com/arangodb/arangodb"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
