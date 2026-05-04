FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.13.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gogs/gogs/releases/download/v${VERSION}/gogs_${VERSION}_linux_amd64.tar.gz" -o /tmp/gogs.tar.gz && \
    echo "75da1c026cacb187a7c1dcad8263873ec566ce30cc0df56dd1dc129b8292d34f  /tmp/gogs.tar.gz" | sha256sum -c - || true
    tar -xzf /tmp/gogs.tar.gz -C /tmp && \
    mv /tmp/gogs /tmp/gogs-bin && chmod +x /tmp/gogs-bin/gogs && strip /tmp/gogs-bin/gogs || true
RUN test -f /tmp/gogs-bin/gogs && test -s /tmp/gogs-bin/gogs || { echo "ERROR: gogs binary not downloaded" >&2; exit 1; }

FROM scratch
COPY --from=downloader /tmp/gogs-bin/gogs /usr/local/bin/gogs
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="gogs" \
      org.opencontainers.image.description="Gogs - lightweight self-hosted Git service" \
      org.opencontainers.image.version="0.13.0" \
      org.opencontainers.image.vendor="Gogs" \
      org.opencontainers.image.source="https://github.com/gogs/gogs" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["gogs"]
