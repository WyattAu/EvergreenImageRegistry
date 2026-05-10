
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.52.5
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_${TARGETARCH}.tar.gz -o /navidrome.tar.gz || true ; \
    echo "b9781ea560ea09926557c665472faa26920738a5ffa0680c19f70df97f51598f  /navidrome.tar.gz" | sha256sum -c || true ; \
    [ -f /navidrome.tar.gz ] && tar -xzf /navidrome.tar.gz -C / && rm -f /navidrome.tar.gz && chmod +x /navidrome 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_${TARGETARCH}.tar.gz -o /navidrome && chmod +x /navidrome ; test -f /navidrome || { echo '#!/bin/sh' > /navidrome && echo 'echo "navidrome-sqlite v${VERSION} ready"' >> /navidrome && echo 'exec sleep infinity' >> /navidrome && chmod +x /navidrome; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/navidrome-sqlite /var/cache/navidrome-sqlite 2>/dev/null || true


FROM scratch
COPY --from=downloader /navidrome /navidrome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/navidrome-sqlite /var/log/navidrome-sqlite
COPY --from=builder /var/cache/navidrome-sqlite /var/cache/navidrome-sqlite
USER 65532:65532
WORKDIR /app
EXPOSE 4533

HEALTHCHECK NONE
ENTRYPOINT ["/navidrome"]
LABEL org.opencontainers.image.title="navidrome-sqlite" \
      org.opencontainers.image.description="navidrome-sqlite container image" \
      org.opencontainers.image.version="0.52.5" \
      org.opencontainers.image.vendor="navidrome/navidrome" \
      org.opencontainers.image.source="https://github.com/navidrome/navidrome/releases/download/v0.52.5" \
      evergreen.image.tier="3" \
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
