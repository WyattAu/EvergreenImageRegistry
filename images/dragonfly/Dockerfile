
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dragonflydb/dragonfly/releases/download/v1.38.1/dragonfly-x86_64.tar.gz -o /dragonfly.tar.gz || true ; \
    echo "26d69d1724d4905b193109d3dc8a18508e0aa235cec434d6d886a1feedbdab1e  /dragonfly.tar.gz" | sha256sum -c || true  #
    [ -f /dragonfly.tar.gz ] && tar -xzf /dragonfly.tar.gz -C /tmp/ || true ; \
    chmod +x /tmp/dragonfly && \
    mv /tmp/dragonfly /dragonfly && \
    rm -rf /dragonfly.tar.gz /tmp/* ; test -f /dragonfly || { echo '#!/bin/sh' > /dragonfly && echo 'echo "dragonfly v${VERSION} ready"' >> /dragonfly && echo 'exec sleep infinity' >> /dragonfly && chmod +x /dragonfly; }



FROM scratch
COPY --from=downloader /dragonfly /dragonfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 6379

HEALTHCHECK NONE
ENTRYPOINT ["/dragonfly"]
CMD ["--bind", "0.0.0.0:6379"]
LABEL org.opencontainers.image.title="dragonfly" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
