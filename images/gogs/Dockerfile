FROM debian:bookworm-slim AS downloader
ARG VERSION=0.13.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gogs/gogs/releases/download/v${VERSION}/gogs_${VERSION}_linux_amd64.tar.gz" -o /tmp/gogs.tar.gz && \
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
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["gogs"]
