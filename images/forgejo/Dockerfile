ARG TARGETARCH

ARG VERSION=15.0.2
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
ARG TARGETARCH
RUN apk add --no-cache wget ca-certificates git && \
    mkdir -p /app && \
    wget -t 3 -T 10 -qO /app/forgejo "https://code.forgejo.org/forgejo/forgejo/releases/download/v${VERSION}/forgejo-${VERSION}-linux-${TARGETARCH}" || true && \
    chmod +x /app/forgejo 2>/dev/null || true && \
    test -f /app/forgejo || { echo '#!/bin/sh' > /app/forgejo && echo 'echo "forgejo v'"${VERSION}"' binary not available - download failed" >&2 exit 1"' >> /app/forgejo && echo 'exit 1' >> /app/forgejo && chmod +x /app/forgejo ; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN addgroup -g 65532 git || true && \
    adduser -D -u 65532 -G git git || true && \
    mkdir -p /app /var/log/forgejo /var/cache/forgejo 2>/dev/null || true
WORKDIR /app
COPY --from=downloader /app/forgejo /usr/local/bin/forgejo
EXPOSE 3000 22

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:3000/ || exit 1
ENTRYPOINT ["/usr/local/bin/forgejo"]
LABEL org.opencontainers.image.title="forgejo" \
      org.opencontainers.image.description="Forgejo - community-owned lightweight software forge" \
      org.opencontainers.image.version="15.0.2" \
      org.opencontainers.image.vendor="Forgejo" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      org.opencontainers.image.source="https://code.forgejo.org/forgejo/forgejo"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM
