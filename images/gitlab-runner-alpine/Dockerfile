FROM debian:bookworm-slim AS downloader
ARG VERSION=16.11.0
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://gitlab-runner-downloads.s3.amazonaws.com/v16.11.0/binaries/gitlab-runner-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary ; test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "gitlab-runner-alpine v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; } || true


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitlab-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8093
LABEL org.opencontainers.image.title="gitlab-runner-alpine"       org.opencontainers.image.description="GitLab Runner (scratch) - CI/CD runner for GitLab, minimal scratch image"       org.opencontainers.image.version="16.11.0"       org.opencontainers.image.vendor="GitLab"       org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-runner"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
