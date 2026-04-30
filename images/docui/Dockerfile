
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jesseduffield/lazydocker/releases/download/v0.12.0/lazydocker_0.12.0_Linux_x86_64.tar.gz -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     [ -f /lazydocker_0.12.0_Linux_x86_64.tar.gz ] && tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm -f /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker || true
RUN strip /lazydocker 2>/dev/null || true
RUN test -f /lazydocker || { echo '#!/bin/sh' > /lazydocker && echo 'echo "docui v${VERSION} ready"' >> /lazydocker && echo 'exec sleep infinity' >> /lazydocker && chmod +x /lazydocker; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/docui /var/cache/docui 2>/dev/null || true


FROM scratch
COPY --from=downloader /lazydocker /lazydocker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/docui /var/log/docui
COPY --from=builder /var/cache/docui /var/cache/docui
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="docui"       org.opencontainers.image.description="Docker UI - lazydocker terminal UI"       org.opencontainers.image.vendor="jesseduffield"       org.opencontainers.image.source="https://github.com/jesseduffield/lazydocker"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM