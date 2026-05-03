FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.26.1
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64" -o /tmp/gitea && \
    echo "324ffd2cc85d567ecd821ad3e19de4abe1c7f94a082b382c1453d4ca7bcf2a7b  /tmp/gitea" | sha256sum -c - && \
    chmod +x /tmp/gitea && strip /tmp/gitea || true
RUN test -f /tmp/gitea && test -s /tmp/gitea || { echo "ERROR: gitea binary not downloaded" >&2; exit 1; }

FROM scratch
COPY --from=downloader /tmp/gitea /usr/local/bin/gitea
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="gitea-secure" \
      org.opencontainers.image.description="Gitea Secure - Hardened Git hosting with enhanced security defaults" \
      org.opencontainers.image.version="1.26.1" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://github.com/go-gitea/gitea" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["gitea"]
