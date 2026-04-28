FROM debian:bookworm-slim AS downloader
ARG VERSION=0.14.2
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gogs/gogs/releases/download/v${VERSION}/gogs_v${VERSION}_linux_amd64.tar.gz -o /tmp/gogs.tar.gz && \
    tar -xzf /tmp/gogs.tar.gz -C /tmp && \
    mv /tmp/gogs /usr/local/bin/gogs && chmod +x /usr/local/bin/gogs && strip /usr/local/bin/gogs


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gogs
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="gogs"       org.opencontainers.image.description="Gogs - lightweight self-hosted Git service"       org.opencontainers.image.version="0.14.2"       org.opencontainers.image.vendor="Gogs"       org.opencontainers.image.source="https://github.com/gogs/gogs"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
